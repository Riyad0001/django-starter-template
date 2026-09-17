from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import (
    SiteSettings, HeroSection, HeroSlide,
    Service, ServiceFeature, WhyUsItem,
    Booking, FooterLink
)


# ─── Inlines ───────────────────────────────────────────────
class ServiceFeatureInline(TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ("text", "order")


# ─── SiteSettings ──────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ("Branding", {
            "fields": ("site_name", "site_tagline", "logo", "favicon"),
        }),
        ("Contact Information", {
            "fields": ("phone", "email", "whatsapp_number"),
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description"),
        }),
        ("Footer", {
            "fields": ("footer_about_text", "copyright_text"),
        }),
        ("Social Media Links", {
            "fields": ("facebook_url", "twitter_url", "instagram_url", "youtube_url"),
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ─── HeroSection ───────────────────────────────────────────
@admin.register(HeroSection)
class HeroSectionAdmin(ModelAdmin):
    fieldsets = (
        ("Main Content", {
            "fields": ("badge_text", "headline", "headline_highlight", "headline_suffix", "description"),
        }),
        ("Call-to-Action Buttons", {
            "fields": ("cta_primary_text", "cta_primary_link", "cta_secondary_text", "cta_secondary_link"),
        }),
        ("Statistics", {
            "fields": (
                "stat1_value", "stat1_label",
                "stat2_value", "stat2_label",
                "stat3_value", "stat3_label",
            ),
        }),
    )

    def has_add_permission(self, request):
        return not HeroSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ─── HeroSlide ─────────────────────────────────────────────
@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = ("title", "subtitle", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)


# ─── Service ───────────────────────────────────────────────
@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ("title", "price", "price_label", "is_popular", "order", "is_active")
    list_editable = ("price", "order", "is_active", "is_popular")
    list_filter = ("is_active", "is_popular")
    search_fields = ("title",)
    inlines = [ServiceFeatureInline]


# ─── WhyUsItem ─────────────────────────────────────────────
@admin.register(WhyUsItem)
class WhyUsItemAdmin(ModelAdmin):
    list_display = ("title", "icon_class", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)


# ─── Booking ──────────────────────────────────────────────
@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ("full_name", "email", "phone", "visa_type", "status", "created_at")
    list_filter = ("status", "visa_type", "created_at")
    list_editable = ("status",)
    search_fields = ("full_name", "email", "phone")
    readonly_fields = ("id", "created_at", "updated_at")
    date_hierarchy = "created_at"

    fieldsets = (
        ("Customer Info", {
            "fields": ("id", "full_name", "email", "phone"),
        }),
        ("Booking Details", {
            "fields": ("visa_type", "message", "status"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )


# ─── FooterLink ───────────────────────────────────────────
@admin.register(FooterLink)
class FooterLinkAdmin(ModelAdmin):
    list_display = ("text", "url", "order", "is_active")
    list_editable = ("order", "is_active")
