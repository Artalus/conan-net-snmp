from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(
        username='Artalus',
        channel='ci',
        upload='https://api.bintray.com/conan/artalus/conan-public',
        stable_branch_pattern='stable/*',
        login_username='Artalus'
    )
    builder.add_common_builds(shared_option_name='net-snmp:shared')
    builder.run()
