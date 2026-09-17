import uuid
from django.db import models
from django.core.exceptions import ValidationError


class SingletonModel(models.Model):
    """Base model that only allows a single instance."""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f"Only one {self.__class__.__name__} instance is allowed.")
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    """Global site settings — editable from admin."""
    site_name = models.CharField(max_length=100, default="SlotBooker")
    site_tagline = models.CharField(max_length=200, default="Your Trusted Visa Partner")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)

    # Contact
    phone = models.CharField(max_length=30, default="+880 1XXXXXXXXX")
    email = models.EmailField(default="info@example.com")
    whatsapp_number = models.CharField(max_length=30, default="+8801XXXXXXXXX",
                                        help_text="Full number with country code, no spaces. e.g. +8801812345678")

    # SEO
    meta_title = models.CharField(max_length=200, default="Visa Slot Booking Services")
    meta_description = models.TextField(default="Professional visa slot booking services for Medical, Tourist, and Double Entry visas", max_length=500)

    # Footer
    footer_about_text = models.TextField(
        default="We provide fast, reliable, and hassle-free visa slot booking services. Your trusted partner for all visa needs.",
        max_length=500
    )
    copyright_text = models.CharField(max_length=200, default="© 2026 SlotBooker. All Rights Reserved.")

    # Social links
    facebook_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class HeroSection(SingletonModel):
    """Hero section content — editable from admin."""
    badge_text = models.CharField(max_length=100, default="⭐ Trusted by 1000+ Customers")
    headline = models.CharField(max_length=200, default="Book Your")
    headline_highlight = models.CharField(max_length=100, default="India Visa",
                                           help_text="This part gets highlighted color")
    headline_suffix = models.CharField(max_length=100, default="Slot Effortlessly")
    description = models.TextField(
        default="Fast, reliable, and hassle-free visa slot booking services for Medical, Tourist, and Double Entry visas across all IVAC centers.",
        max_length=500
    )
    cta_primary_text = models.CharField(max_length=50, default="Explore Services")
    cta_primary_link = models.CharField(max_length=200, default="#services")
    cta_secondary_text = models.CharField(max_length=50, default="Get Help")
    cta_secondary_link = models.CharField(max_length=200, default="#contact")

    # Stats
    stat1_value = models.CharField(max_length=20, default="1000+")
    stat1_label = models.CharField(max_length=50, default="Visas Processed")
    stat2_value = models.CharField(max_length=20, default="99%")
    stat2_label = models.CharField(max_length=50, default="Success Rate")
    stat3_value = models.CharField(max_length=20, default="4.9")
    stat3_label = models.CharField(max_length=50, default="Customer Rating")

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Hero Section"


class HeroSlide(models.Model):
    """Hero background slider images."""
    image = models.ImageField(upload_to="hero/slides/")
    icon_class = models.CharField(max_length=50, default="fas fa-passport",
                                   help_text="Font Awesome class e.g. 'fas fa-passport'")
    title = models.CharField(max_length=100, default="Visa Services")
    subtitle = models.CharField(max_length=100, default="Fast & Reliable")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"

    def __str__(self):
        return f"Slide {self.order}: {self.title}"


class Service(models.Model):
    """Service/pricing cards — editable from admin."""
    icon_class = models.CharField(max_length=50, default="fas fa-passport",
                                   help_text="Font Awesome class e.g. 'fas fa-briefcase-medical'")
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    price_label = models.CharField(max_length=20, default="BDT", help_text="Currency label")
    description = models.TextField(max_length=300, blank=True)
    is_popular = models.BooleanField(default=False, help_text="Show 'Most Popular' badge")
    cta_text = models.CharField(max_length=50, default="Book Now")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class ServiceFeature(models.Model):
    """Feature items listed inside each service card."""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="features")
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Service Feature"
        verbose_name_plural = "Service Features"

    def __str__(self):
        return f"{self.service.title} — {self.text}"


class WhyUsItem(models.Model):
    """Why Choose Us feature cards."""
    icon_class = models.CharField(max_length=50, default="fas fa-bolt",
                                   help_text="Font Awesome class")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Why Choose Us Item"
        verbose_name_plural = "Why Choose Us Items"

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Booking form submissions from the website."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    visa_type = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="bookings")
    message = models.TextField(blank=True, max_length=1000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"{self.full_name} — {self.visa_type} ({self.status})"


class FooterLink(models.Model):
    """Quick links displayed in the footer."""
    text = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Footer Link"
        verbose_name_plural = "Footer Links"

    def __str__(self):
        return self.text
