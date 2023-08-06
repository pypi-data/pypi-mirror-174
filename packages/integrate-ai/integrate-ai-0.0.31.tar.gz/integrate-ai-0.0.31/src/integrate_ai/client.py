from ctypes import Union
import typer
import os
import rich
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn
from integrate_ai.utils.docker_client import DockerClient
from pathlib import Path
from integrate_ai.utils.typer_utils import (
    TogglePromptOption,
    path_param_callback,
)
from integrate_ai.utils.logger import get_log_paths, logs_folder
from integrate_ai.utils.path_utils import get_volumes, get_mounted_path, get_aws_env
from typing import Any, Dict

batch_size_default = 16
instruction_polling_time_default = 30
log_interval_default = 10

app = typer.Typer(no_args_is_help=True)


@app.command()
def pull(
    token: str = TogglePromptOption(
        ...,
        help="The IAI token.",
        prompt="Please provide your IAI token",
        envvar="IAI_TOKEN",
    ),
    version: str = typer.Option("latest", "--version", "-v", help="The version of the docker image to pull."),
    GPU: bool = typer.Option(False, "--GPU/--CPU", help="Specify the GPU or CPU version of the docker image."),
):
    """
    Pull the federated learning docker client.\n Defaults to the latest CPU version. Docker must be running for this command to work.
    """

    no_prompt = os.environ.get("IAI_DISABLE_PROMPTS")
    delete_response = False

    # start progress bar
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:

        # connect to docker
        p = progress.add_task(description="Connecting to docker...", total=1)
        docker_client = DockerClient(token, gpu=GPU)
        progress.update(task_id=p, completed=True)

        # check if any existing docker images on system
        p = progress.add_task(description="Searching for existing client images...", total=1)
        current_images = docker_client.get_local_versions(docker_client.docker_image_name)
        progress.update(task_id=p, completed=True)

        # check for latest docker image
        p = progress.add_task(description="Determining latest available client version...", total=1)
        docker_client.login()
        latest_available_version = docker_client.get_latest_available_version()
        progress.update(task_id=p, completed=True)

    version_to_pull = latest_available_version if version == "latest" else version
    if len(current_images) == 0:
        rprint("No existing client version found on system.")
    else:

        # if images exist on system, check the latest version that is installed
        latest_version = docker_client.get_latest_version_of_image(current_images) or "`latest`"
        if not GPU and "-cpu" not in version_to_pull:
            version_to_pull += "-cpu"

        rprint(
            f"Latest version of docker image found on system is {latest_version}. Most recent version is {latest_available_version}."
        )

        if latest_version == version_to_pull:

            # no point installing if they already have the latest image
            rprint("The requested version of the client image is already on your system. Exiting...")
            raise typer.Exit(0)
        else:
            prompt_msg = f"A newer version {latest_available_version} was found. The current version of the client image will be deleted from your system. Do you want to proceed?"
            # confirm that they are ok with deleting current client images on system
            prompt_msg = "Installing this client image will delete any current version of this image on your system. Do you want to proceed?"
            if no_prompt:
                delete_response = True
            else:
                delete_response = typer.confirm(prompt_msg)

    # delete current client images if they ok'd it
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        if delete_response:
            p = progress.add_task(
                description="Yes response received. Deleting existing client images...",
                total=1,
            )
            docker_client.delete_images(current_images)
            progress.update(task_id=p, completed=True)
        elif not delete_response and len(current_images) > 0:
            rprint("`No` response received. Exiting...")
            raise typer.Exit(0)

    # login and pull docker image
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        p = progress.add_task(description="Logging into docker repo...", total=1)
        login_result = docker_client.login()
        progress.update(task_id=p, completed=True)
        p = progress.add_task(
            description=f"Pulling docker image {version_to_pull}. This will take a few minutes...",
            total=1,
        )
        pull_result = docker_client.pull(repo=docker_client.docker_image_name, tag=version_to_pull)
        progress.update(task_id=p, completed=True)
        rprint(f"Image {version_to_pull} is now available.")
        raise typer.Exit(0)


@app.command()
def version():
    """
    The currently installed version of the docker client image.
    """
    docker_client = DockerClient()
    current_images = docker_client.get_local_versions(docker_client.docker_image_name)
    latest_version = docker_client.get_latest_version_of_image(current_images)
    if len(current_images) == 0:
        rprint("No client image found on system.")
    elif not latest_version:
        rprint("Found version tagged as `latest`.")
    else:
        rprint(latest_version)


@app.command()
def list(
    token: str = TogglePromptOption(
        ...,
        help="The IAI token.",
        prompt="Please provide your IAI token",
        envvar="IAI_TOKEN",
    )
):
    """
    List all available docker client images versions to pull.
    """
    docker_client = DockerClient(token)
    docker_client.login()
    versions = docker_client.get_versions()
    rprint("\n".join(versions))


@app.command()
def log(
    session: str = TogglePromptOption(
        ...,
        help="The session id to fetch logs for.",
        prompt="Please provide the training session id",
        envvar="IAI_SESSION",
    ),
    client_name: str = TogglePromptOption(
        ...,
        help="The name of the client container used for training.",
        prompt="Please provide the client container name",
    ),
):
    """
    This command fetches logs of the client docker container for debugging purposes.
    """
    # form path and check if it exists
    session_log_path, client_log_path = get_log_paths(client_name=client_name, session=session)

    rprint(f"Checking if session logs are available at {logs_folder}")
    if os.path.exists(client_log_path):
        print("Log file found:")
        with open(client_log_path, "r") as f:
            contents = f.read()
        rprint(contents)
    if os.path.exists(logs_folder) is False:
        print("Seems like there are no logs, try running a session!")
    if os.path.exists(session_log_path) is False:  # check if session log exists
        print(f"Log files for this session: {session} does not exist")
    if os.path.exists(client_log_path) is False:  # check if client log exists
        print(f"Log file for client: {client_name} does not exist")

    raise typer.Exit(0)


@app.command()
def train(
    token: str = TogglePromptOption(
        ...,
        help="Your generated IAI token.",
        prompt="Please provide your IAI token",
        envvar="IAI_TOKEN",
    ),
    session: str = TogglePromptOption(
        ...,
        help="The session id to join for training.",
        prompt="Please provide the training session id",
        envvar="IAI_SESSION",
    ),
    train_path=TogglePromptOption(
        ...,
        help="Training dataset path or s3 URL.",
        prompt="Please provide the training dataset pathi or s3 URL",
    ),
    test_path=TogglePromptOption(
        ...,
        help="Testing dataset path or s3 URL.",
        prompt="Please provide the testing dataset path or s3 URL",
    ),
    client_name: str = TogglePromptOption(
        ...,
        help="The name used for client container.",
        prompt="Please provide the client container name",
    ),
    batch_size: int = typer.Option(batch_size_default, "--batch-size", help="Batch size to load the data with."),
    instruction_polling_time: int = typer.Option(
        instruction_polling_time_default,
        "--instruction-polling-time",
        help="Time to wait for new instructions in seconds.",
    ),
    log_interval: int = typer.Option(
        log_interval_default,
        "--log-interval",
        help="The logging frequency for training printout.",
    ),
    approve_custom_package: bool = typer.Option(
        False,
        "--approve-custom-package",
        help="Flag to give pre-approval for training custom model package.",
    ),
    remove_after_complete: bool = typer.Option(
        False,
        "--remove-after-complete",
        help="Flag to remove container after training completed",
    ),
    verbose: bool = typer.Option(False, "--verbose", help="Enables debug logging."),
):
    """
    Join a training session using the docker client.
    The client docker container will be deleted on completion.
    The following environment variables will be passed into the docker container:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION.
    This way code running inside the container can take advantage of AWS APIs, e.g. reading
    data from S3.
    """
    train_path = path_param_callback(train_path)
    test_path = path_param_callback(test_path)

    docker_client = DockerClient()
    container_name = str(client_name)
    mounted_data_path, local_log_path = mount_and_start_docker(
        docker_client, container_name, session, "train", train_path=train_path, test_path=test_path
    )
    mounted_train_path = mounted_data_path["mounted_train_path"]
    mounted_test_path = mounted_data_path["mounted_test_path"]

    cmd = f"hfl train --token {token} --session-id {session}"
    cmd += f" --train-path {mounted_train_path}"
    cmd += f" --test-path {mounted_test_path}"
    cmd += f" --batch-size {batch_size}"
    cmd += f" --instruction-polling-time {instruction_polling_time}"
    cmd += f" --log-interval {log_interval}"
    if approve_custom_package:
        cmd += " --approve-custom-package"

    container = docker_client.get_container(container_name)
    environment = get_aws_env(train_path)
    if environment == {}:
        environment.update(get_aws_env(test_path))

    excute_command_and_close_docker(container, cmd, environment, local_log_path, remove_after_complete, verbose)


@app.command()
def eda(
    token: str = TogglePromptOption(
        ...,
        help="Your generated IAI token.",
        prompt="Please provide your IAI token",
        envvar="IAI_TOKEN",
    ),
    session: str = TogglePromptOption(
        ...,
        help="The session id to join for EDA.",
        prompt="Please provide the EDA session id",
        envvar="IAI_SESSION",
    ),
    dataset_path=TogglePromptOption(
        ...,
        help="EDA dataset path or s3 URL.",
        prompt="Please provide the EDA dataset path or s3 URL",
    ),
    dataset_name: str = TogglePromptOption(
        ...,
        help="The name of the dataset.",
        prompt="Please provide a dataset name",
    ),
    remove_after_complete: bool = typer.Option(
        False,
        "--remove-after-complete",
        help="Flag to remove container after eda session completed",
    ),
    instruction_polling_time: int = typer.Option(
        instruction_polling_time_default,
        "--instruction-polling-time",
        help="Time to wait for new instructions in seconds.",
    ),
    log_interval: int = typer.Option(
        log_interval_default,
        "--log-interval",
        help="The logging frequency for EDA session printout.",
    ),
    verbose: bool = typer.Option(False, "--verbose", help="Enables debug logging."),
):
    """
    Join a eda session using the docker client.
    The client docker container will be deleted on completion.
    The following environment variables will be passed into the docker container:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION.
    This way code running inside the container can take advantage of AWS APIs, e.g. reading
    data from S3.
    """
    dataset_path = path_param_callback(dataset_path)
    docker_client = DockerClient()
    container_name = str(dataset_name)
    mounted_data_path, local_log_path = mount_and_start_docker(
        docker_client, container_name, session, "eda", dataset_path=dataset_path
    )
    mounted_dataset_path = mounted_data_path["mounted_dataset_path"]

    cmd = f"hfl eda --token {token} --session-id {session}"
    cmd += f" --dataset-name {dataset_name}"
    cmd += f" --dataset-path {mounted_dataset_path}"
    cmd += f" --instruction-polling-time {instruction_polling_time}"
    cmd += f" --log-interval {log_interval}"

    container = docker_client.get_container(container_name)
    environment = get_aws_env(dataset_path)

    excute_command_and_close_docker(container, cmd, environment, local_log_path, remove_after_complete, verbose)


def mount_and_start_docker(docker_client: DockerClient, container_name: str, session: str, command: str, **kwargs):
    """Mount data paths to docker and start docker container

    Args:
        docker_client (DockerClient): A DockerClient object
        container_name (str): Name of the container
        session (str): Session id
        command (str):  Can be either eda or train
        kwargs:
            train_path (Dict): Training data path for train command
            test_path (Dict): Testing data path for train command
            dataset_path (Dict): Data path for eda command

    Returns:
        mounted_data_path (Dict): Mounted data path
        local_log_path (str): Full path to the client log file
    """
    current_images = docker_client.get_local_versions(docker_client.docker_image_name)
    latest_version = docker_client.get_latest_version_of_image(current_images)

    mount_path = "/root/"

    if len(current_images) == 0:
        rich.print("No client image found on system.")
        rich.print("Exiting...")
        raise typer.Exit(0)

    image_name = f"{docker_client.docker_image_name}"
    if latest_version:
        image_name += ":" + latest_version

    ## Adding a conatiner path for logging, this is mounted later

    session_log_folder, local_log_path = get_log_paths(client_name=container_name, session=session)
    container_log_path = mount_path + f"iai/logs/{container_name}.log"

    # Create full path to log file if it does not exist
    os.makedirs(session_log_folder, exist_ok=True)
    # Creates an empty file
    file = open(local_log_path, "w")
    file.close()

    volumes = {}
    # Bind local log path to folder on container
    volumes[local_log_path] = {"bind": container_log_path, "mode": "rw"}
    command_map = {"train": mount_data_for_train, "eda": mount_data_for_eda}
    volumes, mounted_data_path = command_map[command](mount_path, volumes, **kwargs)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        start_container_task = progress.add_task(description=f"Starting container {container_name}...", total=1)
        try:
            response = docker_client.run(
                image_name,
                detach=True,
                options={
                    "tty": True,
                    "name": container_name,
                    "volumes": volumes,
                    "environment": {"IAI_LOG_SAVE_PATH": container_log_path},
                    "extra_hosts": {"localhost": "host-gateway"},
                },
            )
        except Exception as e:
            progress.console.print(e, style="red")
            raise typer.Exit(0)

        progress.update(task_id=start_container_task, completed=True)
        progress.console.print(f"Container {container_name} is started.", style="green")
    return mounted_data_path, local_log_path


def mount_data_for_train(mount_path, volumes, **kwargs):
    """Mount data paths for train command

    Args:
        mount_path (DockerClient): A DockerClient object
        volumes (str): Volumes for docker container
        kwargs:
            train_path (Dict): Training data path for train command
            test_path (Dict): Testing data path for train command

    Returns:
        volumes (Dict): Binded volumes for local paths
        mounted_data_path (Dict): Mounted data paths
    """
    train_path = kwargs.get("train_path")
    test_path = kwargs.get("test_path")
    mounted_train_path = get_mounted_path(mount_path, train_path)
    mounted_test_path = get_mounted_path(mount_path, test_path)
    # Bind volumes for local paths
    volumes = {
        **volumes,
        **get_volumes(mount_path, train_path),
        **get_volumes(mount_path, test_path),
    }
    mounted_data_path = {
        "mounted_train_path": mounted_train_path,
        "mounted_test_path": mounted_test_path,
    }
    return volumes, mounted_data_path


def mount_data_for_eda(mount_path, volumes, **kwargs):
    """Mount data paths for eda command

    Args:
        mount_path (DockerClient): A DockerClient object
        volumes (str): Volumes for docker container
        kwargs:
            dataset_path (Dict): Dataset_path data path for eda command

    Returns:
        volumes (Dict): Binded volumes for local paths
        mounted_data_path (Dict): Mounted data paths
    """
    dataset_path = kwargs.get("dataset_path")
    mounted_dataset_path = get_mounted_path(mount_path, dataset_path)
    # Bind volumes for local paths
    volumes = {
        **volumes,
        **get_volumes(mount_path, dataset_path),
    }
    mounted_data_path = {
        "mounted_dataset_path": mounted_dataset_path,
    }
    return volumes, mounted_data_path


def set_env_var(environment, env_var_name):
    """Update the dict of existing environment variables to include `env_var_name`,
    if it is set in the current environment.

    Args:
        environment (Dict): the dictionary of existing environment variables
        env_var_name (str): the new env variable to add
    """
    env_var_value = os.getenv(env_var_name)
    if env_var_value:
        environment.update({env_var_name: env_var_value})


def excute_command_and_close_docker(container, cmd, environment, local_log_path, remove_after_complete, verbose):
    """Excute eda or train command and close the container when complete

    Args:
        container : A Container object
        cmd : Command to be execute
        environment : AWS environment variable to pass in the container
        local_log_path :  Full path to the client log file
        remove_after_complete: Remove the container after complete when equals True
        verbose: Log verbose for container

    """
    set_env_var(environment, "IAI_DEBUG_LOCAL_GATEWAY")
    set_env_var(environment, "IAI_FLOUR_LOG_LEVEL")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task(description=f"Processing...", total=1)
        response = container.exec_run(
            cmd,
            stdout=verbose,
            stream=True,
            demux=True,
            environment=environment,
        )
        if response:
            for (output, error) in response.output:  # type: ignore
                if error:
                    progress.console.print(error.decode("utf-8"))
                else:
                    progress.console.print(output.decode("utf-8"))

        progress.update(task_id=task, completed=True)

    progress.console.print(f"Finished processing.", style="green")
    progress.console.print(f"Logs are saved in {local_log_path} and can be found with iai client log", style="blue")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        closing_task = progress.add_task(description=f"Closing container...", total=1)
        container.stop()
        if remove_after_complete:
            container.remove()
        progress.update(task_id=closing_task, completed=True)

        raise typer.Exit(0)


@app.callback()
def main():
    """
    Sub command for managing client related operations.
    """
