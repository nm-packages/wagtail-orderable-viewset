from django.core.management.base import BaseCommand
import random
from faker import Faker

from home.models import Testimonial, TeamMember, Person


class Command(BaseCommand):
    help = "Create sample data for testing wagtail-orderable-viewset"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=50, help="Minimum records per model"
        )
        parser.add_argument(
            "--seed", type=int, default=1337, help="Random seed (for reproducibility)"
        )
        parser.add_argument(
            "--delete-existing",
            action="store_true",
            help="Delete existing records for all models before creating new ones",
        )
        parser.add_argument(
            "--clear-only",
            action="store_true",
            help="Delete all existing records for all models and exit without creating new data",
        )

    def handle(self, *args, **options):
        target = int(options["count"])
        seed = int(options["seed"])
        delete_existing = bool(options.get("delete_existing"))
        clear_only = bool(options.get("clear_only"))
        random.seed(seed)
        faker = Faker()
        faker.seed_instance(seed)

        self.stdout.write(
            f"Creating sample data (ensuring at least {target} records per model)..."
        )

        # Optionally delete existing data first
        if delete_existing or clear_only:
            self.stdout.write("Deleting existing records...")
            t_count = Testimonial.objects.count()
            tm_count = TeamMember.objects.count()
            p_count = Person.objects.count()
            Testimonial.objects.all().delete()
            TeamMember.objects.all().delete()
            Person.objects.all().delete()
            self.stdout.write(f" - Deleted Testimonials: {t_count}")
            self.stdout.write(f" - Deleted Team members: {tm_count}")
            self.stdout.write(f" - Deleted People: {p_count}")
            if clear_only:
                self.stdout.write(self.style.SUCCESS("All records cleared."))
                return

        # Testimonials (uses sort_order)
        existing = Testimonial.objects.count()
        if existing < target:
            to_create = []
            for i in range(existing, target):
                name = faker.name()
                company = faker.company()
                content = faker.paragraph(nb_sentences=3)
                rating = random.randint(3, 5)
                is_featured = random.random() < 0.25
                sort_order = i + 1
                to_create.append(
                    Testimonial(
                        name=name,
                        company=company,
                        content=content,
                        rating=rating,
                        is_featured=is_featured,
                        sort_order=sort_order,
                    )
                )
            Testimonial.objects.bulk_create(to_create)
            self.stdout.write(f"Added {len(to_create)} testimonials (total: {target}).")
        else:
            self.stdout.write(f"Testimonials already >= {target} (total: {existing}).")

        # Team members (uses sort_order)
        existing = TeamMember.objects.count()
        if existing < target:
            to_create = []
            roles = [
                "Engineer",
                "Designer",
                "Product Manager",
                "Data Analyst",
                "DevOps",
                "QA Engineer",
                "Support Specialist",
                "Tech Writer",
                "Architect",
                "Team Lead",
            ]
            for i in range(existing, target):
                name = faker.name()
                bio = faker.paragraph(nb_sentences=2)
                position = random.choice(roles)
                email = faker.unique.email()
                sort_order = i + 1
                to_create.append(
                    TeamMember(
                        name=name,
                        position=position,
                        bio=bio,
                        email=email,
                        sort_order=sort_order,
                    )
                )
            TeamMember.objects.bulk_create(to_create)
            self.stdout.write(f"Added {len(to_create)} team members (total: {target}).")
        else:
            self.stdout.write(f"Team members already >= {target} (total: {existing}).")

        # People (snippet, uses sort_order)
        existing = Person.objects.count()
        if existing < target:
            to_create = []
            cities = [
                "New York",
                "London",
                "Paris",
                "Berlin",
                "Tokyo",
                "Sydney",
                "Toronto",
                "San Francisco",
                "Amsterdam",
                "Copenhagen",
            ]
            teams = ["engineering", "marketing", "sales", "support", "hr"]
            for i in range(existing, target):
                name = faker.name()
                age = random.randint(18, 80)
                city = random.choice(cities)
                team = random.choice(teams)
                # Skew towards active, but introduce some inactive records for filtering UI
                is_active = random.random() < 0.85
                sort_order = i + 1
                to_create.append(
                    Person(
                        name=name,
                        age=age,
                        city=city,
                        team=team,
                        is_active=is_active,
                        sort_order=sort_order,
                    )
                )
            Person.objects.bulk_create(to_create)
            self.stdout.write(f"Added {len(to_create)} people (total: {target}).")
        else:
            self.stdout.write(f"People already >= {target} (total: {existing}).")

        self.stdout.write(self.style.SUCCESS("Sample data creation complete."))
