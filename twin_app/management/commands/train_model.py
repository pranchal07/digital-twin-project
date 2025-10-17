from django.core.management.base import BaseCommand
from twin_app.ml.model_train import train_model


class Command(BaseCommand):
    help = 'Train the health risk prediction model'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting model training...'))

        try:
            model = train_model()
            self.stdout.write(
                self.style.SUCCESS('Model training completed successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Model training failed: {str(e)}')
            )
