from django.core.management.base import BaseCommand
from apps.core.models import (
    SiteSettings, HeroSection, HeroSlide,
    Service, ServiceFeature, WhyUsItem, FooterLink
)


class Command(BaseCommand):
    help = "Populate initial data for the visa slot booking website"

    def handle(self, *args, **options):
        self.stdout.write("Setting up initial data...")

        # ─── SiteSettings ──────────────────────────────────
        site, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            self.stdout.write(self.style.SUCCESS("✓ SiteSettings created"))
        else:
            self.stdout.write("  SiteSettings already exists")

        # ─── HeroSection ───────────────────────────────────
        hero, created = HeroSection.objects.get_or_create(pk=1)
        if created:
            self.stdout.write(self.style.SUCCESS("✓ HeroSection created"))
        else:
            self.stdout.write("  HeroSection already exists")

        # ─── HeroSlides ────────────────────────────────────
        slides_data = [
            {"icon_class": "fas fa-passport", "title": "Visa Services", "subtitle": "Fast & Reliable", "order": 0},
            {"icon_class": "fas fa-plane", "title": "Travel Ready", "subtitle": "Book Your Slot Now", "order": 1},
            {"icon_class": "fas fa-globe-asia", "title": "All Centers", "subtitle": "Nationwide Coverage", "order": 2},
        ]
        if not HeroSlide.objects.exists():
            for data in slides_data:
                HeroSlide.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f"✓ {len(slides_data)} HeroSlides created"))
        else:
            self.stdout.write("  HeroSlides already exist")

        # ─── Services ──────────────────────────────────────
        services_data = [
            {
                "icon_class": "fas fa-briefcase-medical",
                "title": "Medical Visa",
                "price": 500,
                "description": "Quick slot booking for medical visa applicants",
                "is_popular": False,
                "order": 0,
                "features": [
                    "IVAC Slot Booking",
                    "Application Assistance",
                    "Document Guidance",
                    "Fast Processing",
                    "Email Confirmation",
                ]
            },
            {
                "icon_class": "fas fa-suitcase-rolling",
                "title": "Tourist Visa",
                "price": 500,
                "description": "Hassle-free tourist visa slot booking service",
                "is_popular": True,
                "order": 1,
                "features": [
                    "IVAC Slot Booking",
                    "Priority Processing",
                    "Document Checklist",
                    "Application Review",
                    "24/7 Support",
                    "Money Back Guarantee",
                ]
            },
            {
                "icon_class": "fas fa-passport",
                "title": "Double Entry Visa",
                "price": 800,
                "description": "Multiple entry visa slot booking with premium support",
                "is_popular": False,
                "order": 2,
                "features": [
                    "IVAC Slot Booking",
                    "Premium Processing",
                    "Complete Document Assistance",
                    "Multiple Entry Support",
                    "Dedicated Agent",
                ]
            },
        ]
        if not Service.objects.exists():
            for sdata in services_data:
                features = sdata.pop("features")
                service = Service.objects.create(**sdata)
                for i, feat_text in enumerate(features):
                    ServiceFeature.objects.create(service=service, text=feat_text, order=i)
            self.stdout.write(self.style.SUCCESS(f"✓ {len(services_data)} Services with features created"))
        else:
            self.stdout.write("  Services already exist")

        # ─── WhyUsItems ────────────────────────────────────
        why_data = [
            {"icon_class": "fas fa-bolt", "title": "Fastest Booking", "description": "Get your visa slot booked within minutes with our lightning-fast booking system.", "order": 0},
            {"icon_class": "fas fa-user-tie", "title": "Expert Team", "description": "Our experienced team guides you through every step of the visa process.", "order": 1},
            {"icon_class": "fas fa-tags", "title": "Affordable Prices", "description": "Competitive pricing with no hidden charges. Pay only for what you need.", "order": 2},
            {"icon_class": "fas fa-headset", "title": "24/7 Support", "description": "Round-the-clock customer support via phone, email, and WhatsApp.", "order": 3},
            {"icon_class": "fas fa-map-marked-alt", "title": "All IVAC Centers", "description": "We cover all IVAC centers across Bangladesh for your convenience.", "order": 4},
            {"icon_class": "fas fa-chart-line", "title": "99% Success Rate", "description": "Our proven track record speaks for itself with near-perfect success rates.", "order": 5},
        ]
        if not WhyUsItem.objects.exists():
            for data in why_data:
                WhyUsItem.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f"✓ {len(why_data)} WhyUsItems created"))
        else:
            self.stdout.write("  WhyUsItems already exist")

        # ─── FooterLinks ───────────────────────────────────
        links_data = [
            {"text": "Privacy Policy", "url": "#", "order": 0},
            {"text": "Terms of Service", "url": "#", "order": 1},
            {"text": "FAQ", "url": "#", "order": 2},
        ]
        if not FooterLink.objects.exists():
            for data in links_data:
                FooterLink.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f"✓ {len(links_data)} FooterLinks created"))
        else:
            self.stdout.write("  FooterLinks already exist")

        self.stdout.write(self.style.SUCCESS("\n✅ Initial data setup complete!"))
        self.stdout.write("   Visit /admin/ to customize all content.")
