from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.core.models import (
    SiteSettings, HeroSection, HeroSlide,
    Service, WhyUsItem, Booking, FooterLink
)


def home_view(request):
    """Render the public homepage with all dynamic content."""
    context = {
        "hero": HeroSection.objects.first(),
        "slides": HeroSlide.objects.filter(is_active=True),
        "services": Service.objects.filter(is_active=True).prefetch_related("features"),
        "why_us_items": WhyUsItem.objects.filter(is_active=True),
        "footer_links": FooterLink.objects.filter(is_active=True),
    }
    return render(request, "website/home.html", context)


@require_POST
def submit_booking(request):
    """Handle AJAX booking form submission."""
    try:
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        visa_type_id = request.POST.get("visa_type", "").strip()
        message = request.POST.get("message", "").strip()

        # Basic validation
        errors = {}
        if not full_name:
            errors["full_name"] = "Full name is required."
        if not email:
            errors["email"] = "Email is required."
        if not phone:
            errors["phone"] = "Phone number is required."

        if errors:
            return JsonResponse({"success": False, "errors": errors}, status=400)

        # Get visa type
        visa_type = None
        if visa_type_id:
            try:
                visa_type = Service.objects.get(id=visa_type_id)
            except Service.DoesNotExist:
                pass

        # Create booking
        booking = Booking.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            visa_type=visa_type,
            message=message,
        )

        return JsonResponse({
            "success": True,
            "message": "Thank you! Your booking request has been submitted successfully. We will contact you shortly.",
            "booking_id": str(booking.id),
        })

    except Exception as e:
        return JsonResponse({"success": False, "message": "Something went wrong. Please try again."}, status=500)
