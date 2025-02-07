from utils import (get_log_lines, is_vshard_bootstrapped,
                   run_command_and_get_output)


def test_bootstrap(cartridge_cmd, project_with_vshard_replicasets):
    project = project_with_vshard_replicasets.project
    instances = project_with_vshard_replicasets.instances

    # bootstrap vshard
    cmd = [
        cartridge_cmd, 'replicasets', 'bootstrap-vshard',
    ]

    rc, output = run_command_and_get_output(cmd, cwd=project.path)
    assert rc == 0

    assert get_log_lines(output) == [
        "• Vshard is bootstrapped successfully"
    ]

    router = instances['router']
    admin_api_url = router.get_admin_api_url()
    assert is_vshard_bootstrapped(admin_api_url)

    # bootstrap again
    cmd = [
        cartridge_cmd, 'replicasets', 'bootstrap-vshard',
    ]

    rc, output = run_command_and_get_output(cmd, cwd=project.path)
    assert rc == 1

    assert "already bootstrapped" in output


def test_no_vshard_roles_avaliable(cartridge_cmd, project_with_replicaset_no_roles):
    project = project_with_replicaset_no_roles.project

    # bootstrap vshard
    cmd = [
        cartridge_cmd, 'replicasets', 'bootstrap-vshard',
    ]

    rc, output = run_command_and_get_output(cmd, cwd=project.path)
    assert rc == 1

    assert 'No remotes with role "vshard-router" available' in output


def test_boostrap_vshard_without_setup(cartridge_cmd, project_with_instances):
    project = project_with_instances.project

    # bootstrap vshard without joined instances
    cmd = [
        cartridge_cmd, 'replicasets', 'bootstrap-vshard',
    ]

    rc, output = run_command_and_get_output(cmd, cwd=project.path)
    assert rc == 1
    assert "No instances joined to cluster found" in output
