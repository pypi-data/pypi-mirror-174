from subprocess import PIPE, Popen


def _exec(command, env):
    p = Popen(
        command,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        env=env,
    )
    stdout, stderr = p.communicate()

    if stderr:
        print("EXEC ERROR", command, stdout, stderr)
    return stdout, stderr


def _ctx(db_conf):
    env = {"PGPASSWORD": db_conf["PASSWORD"]}
    try:
        database = db_conf["TEST"]["NAME"] or db_conf["NAME"]
    except KeyError:
        database = db_conf["NAME"]

    data = {
        "host": db_conf["HOST"],
        "port": db_conf["PORT"],
        "user": db_conf["USER"],
        "database": database,
    }
    return data, env


def load(db_conf, input_file):
    ctx, env = _ctx(db_conf)
    command = "psql -h {host} -p {port} -U {user} -d {database} -f {input_file}"
    _exec(command.format(input_file=input_file, **ctx), env)


def dump(db_conf, output_file):
    ctx, env = _ctx(db_conf)
    pg_dump = "pg_dump -Fp -h {host} -p {port} -U {user} -d {database} -f {output_file}"
    _exec(pg_dump.format(output_file=output_file, **ctx), env)
