"""
deploy.py

Deploy services in either Google Cloud Run or CDF Functions.
Model registry uses CDF Files.
"""
import os
import traceback
from pathlib import Path
from typing import List

import akerbp.mlops.model_manager as mm
from akerbp.mlops import __version__ as package_version
from akerbp.mlops.cdf import helpers as cdf
from akerbp.mlops.core import config, logger
from akerbp.mlops.core.config import ServiceSettings
from akerbp.mlops.deployment import helpers
from akerbp.mlops.core.exceptions import TestError, DeploymentError, MLOpsError

# Global variables
logging = logger.get_logger(name="mlops_deployment")

api_keys = config.api_keys
cdf_client = cdf.get_client(
    api_key=api_keys["functions"]
)  # for creating the schedule keeping the functions warm

logging.info(
    f"Deploying prediction service using MLOps framework version {package_version}"
)


def deploy_model(
    model_settings: ServiceSettings,
) -> str:
    """
    Deploy a model.

    This will create a deployment folder and change current working directory
    to it.

    Return "OK" if deployment was successful, otherwise return a string with the traceback for the failed deployment

    Args:
        model_settings (ServiceSettings): settings for the model service
        platform_methods (dict): where key is the platform and value is a tuple with deploy and test functions.
            Defaults to the globally set platform_methods variable.

    Returns:
        (str): status of the deployment
    """
    try:
        c = model_settings
        env = config.envs.env
        testing_only = eval(config.envs.testing_only)
        local_deployment = eval(config.envs.local_deployment)
        service_name = config.envs.service_name
        deployment_folder = helpers.deployment_folder_path(c.model_name)
        function_name = f"{c.model_name}-{service_name}-{env}"

        logging.info(
            f"Starting deployment and/or testing of model {c.human_friendly_model_name}"
        )

        if (service_name == "prediction") and c.artifact_folder:
            mm.set_active_dataset(c.dataset)
            c.model_id = mm.set_up_model_artifact(c.artifact_folder, c.model_name)

        logging.info("Create deployment folder and move required files/folders")
        deployment_folder.mkdir()
        helpers.copy_to_deployment_folder(c.files, deployment_folder)

        logging.debug(f"cd {deployment_folder}")
        os.chdir(deployment_folder)

        # Local testing - for ENV=dev and LOCAL_DEPLOYMENT=False
        if c.platform == "local":
            if c.test_file:
                logging.info("Performing local testing")
                helpers.run_tests(c, setup_venv=True)
            else:
                logging.warning(
                    "No test file specified in the settings, skipping local tests."
                )

        # Deploy to CDF
        elif c.platform == "cdf":
            if (env == "test" or env == "prod") and testing_only is True:
                logging.info(
                    f"Running tests for model {c.human_friendly_model_name} in {env}, will not deploy"
                )
                helpers.run_tests(c, setup_venv=True)
            elif (
                (env == "test" or env == "prod") and testing_only is False
            ) or local_deployment is True:
                # Run unit tests and get test payload before deploying
                logging.info(
                    f"Running tests for model {c.human_friendly_model_name} before deploying to {env}"
                )
                test_payload = helpers.run_tests(c, setup_venv=False)
                (
                    external_id,
                    artifact_version,
                    latest_artifact_version,
                ) = helpers.deploy_model(
                    c,
                    env,
                    service_name,
                    function_name,
                    test_payload=test_payload,
                )

                # Redeploy latest function with a predictable external id (model-service-env)
                if artifact_version == latest_artifact_version:
                    logging.info(
                        f"Redeploying latest model {c.human_friendly_model_name} with predictable external id {function_name} to {c.platform}"
                    )
                    helpers.redeploy_model_with_predictable_external_id(
                        c,
                        external_id=external_id,
                        predictable_external_id=function_name,
                        test_payload=test_payload,
                    )
                else:
                    logging.info(
                        f"Deployment is based on an old artifact version ({artifact_version}/{latest_artifact_version}). Skipping redeployment with a predictable external id."
                    )

                logging.info("Initiating garbage collection of old model versions")
                helpers.garbage_collection(
                    c,
                    function_name,
                    env,
                    cdf_client,
                )
            else:
                logging.warning(
                    f"Will not run tests nor deploy model(s), check your environment variables: {config.envs}"
                )

        # Create a schedule for keeping the latest function warm in prod
        if env == "prod" and c.platform == "cdf":
            logging.info(
                f"Creating a schedule for keeping the function {function_name} warm on weekdays during extended working hours"
            )
            helpers.setup_schedule_for_latest_model_in_prod(
                c,
                predictable_external_id=function_name,
                client=cdf_client,
            )
        return "OK"
    except (
        TestError,
        DeploymentError,
        MLOpsError,
    ):
        trace = traceback.format_exc()
        return f"Model failed to deploy and/or tests failed! See the following traceback for more info: \n\n{trace}"


def deploy(project_settings: List[ServiceSettings]) -> None:
    """
    Deploy a machine learning project that potentially contains multiple models.
    Deploy each model in the settings and make sure that if one model fails it
    does not affect the rest. At the end, if any model failed, it raises an
    exception with a summary of all models that failed.

    Args:
        Project settings as described by the user in the config file.

    Raises:
        Exception: If any model failed to deploy.
    """
    failed_models = {}
    cwd_path = Path.cwd()

    for c in project_settings:
        status = deploy_model(c)
        if status != "OK":
            logging.error(status)
            failed_models[c.human_friendly_model_name] = status

        logging.debug("cd ..")
        os.chdir(cwd_path)
        helpers.rm_deployment_folder(c.model_name)

    if failed_models:
        for model, message in failed_models.items():
            logging.warning(f"Model {model} failed: {message}")
        raise Exception("At least one model failed.")


if __name__ == "__main__":
    mm.setup()
    settings = config.read_project_settings()
    deploy(settings)
