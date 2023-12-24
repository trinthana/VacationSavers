from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from rest_framework.authtoken.models import Token

from ...models import MultiToken
from ...utils import get_user_primary_token


class Command(BaseCommand):
    help = "Sync DRF Auth Tokens to Multi Tokens"

    def add_arguments(self, parser):
        parser.add_argument(
            "--backwards",
            action="store_true",
            default=False,
            help="Sync Multi Tokens back to DRF Auth Tokens. WARNING - If you have created multiple "
            "MultiTokens per User, only the primary MultiToken (which is the newest active MultiToken) "
            "will be created in the DRF Auth Token table. This means existing DRF Auth Tokens may be "
            "overridden. Use with caution.",
        )

    def handle(self, *args, **options):
        created_count = 0
        recreated_count = 0
        existed_count = 0

        if options["backwards"]:
            for user in get_user_model().objects.all():
                multi_token = get_user_primary_token(user)

                if multi_token:
                    drf_token, created = Token.objects.get_or_create(
                        user=user,
                        defaults={
                            "key": multi_token.key,
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        if drf_token.key != multi_token.key:
                            with transaction.atomic():
                                drf_token.delete()
                                drf_token = Token.objects.create(
                                    key=multi_token.key,
                                    user=user,
                                )
                            recreated_count += 1
                        else:
                            existed_count += 1

        else:
            for drf_token in Token.objects.all().iterator():
                multi_token, created = MultiToken.objects.get_or_create(
                    key=drf_token.key,
                    user=drf_token.user,
                )

                if created:
                    created_count += 1
                else:
                    existed_count += 1

        self.stdout.write(
            "Copied {} tokens{}, {} already existed".format(
                created_count,
                f", {recreated_count} keys updated" if recreated_count else "",
                existed_count,
            )
        )
