from lumipy.provider.setup import setup, VERSION_TARGET
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        choices=['setup'],
        help='The lumipy.providers action to run. Available actions are: [setup] sets up the python providers. '
             'This will install/update the dotnet tool and (optionally) copy your certs to the tool\'s directory.'
    )
    parser.add_argument(
        '--certs_path',
        dest='certs_path',
        default=None,
        help='The path to your luminesce .pem files. Optional, but you\'ll need to use lumipy.provider.copy_certs '
             'later before you run anything.'
    )
    parser.add_argument(
        '--version',
        dest='version',
        default=VERSION_TARGET,
        help=f'The version of the dotnet tool to install. Optional, defaults to {VERSION_TARGET}'
    )
    parser.add_argument(
        '--verbosity',
        dest='verbosity',
        default='m',
        help='verbosity of the dotnet install process. Allowed values are q[uiet], m[inimal], n[ormal], d[etailed], '
             'and diag[nostic]. Defaults to "m".'
    )
    args = parser.parse_args()

    if args.action == 'setup':
        setup(args.certs_path, args.version, args.verbosity)
