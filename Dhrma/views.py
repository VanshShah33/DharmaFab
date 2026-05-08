import calendar

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import DatabaseError
from django.db.utils import OperationalError, ProgrammingError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import Company, Contact, Gallery, Inquiry, Manufacturing, Newsletter, Product


FABRIC_CATALOG = {
    'cotton-fabric': {
        'name': 'Cotton Fabric',
        'category': 'Cotton',
        'image': 'images/p1.jpg',
        'description': 'Soft, breathable long-staple cotton for apparel and premium everyday wear.',
    },
    'silk-fabric': {
        'name': 'Silk Fabric',
        'category': 'Silk',
        'image': 'images/p2.jpg',
        'description': 'High-sheen silk texture for couture, occasion wear, and luxury drapery.',
    },
    'premium-denim': {
        'name': 'Premium Denim',
        'category': 'Denim',
        'image': 'images/p4.jpg',
        'description': 'Reinforced twill denim for durable fashion and heavy-use collections.',
    },
    'industrial-fabric': {
        'name': 'Industrial Fabric',
        'category': 'Industrial',
        'image': 'images/p5.jpg',
        'description': 'Technical fabric made for strength, consistency, and specialised applications.',
    },
    'jacquard-weave': {
        'name': 'Jacquard Weave',
        'category': 'Jacquard',
        'image': 'images/p3.jpg',
        'description': 'Custom motif-ready Jacquard weaving for premium and private-label projects.',
    },
}


def _is_valid_email(email):
    try:
        validate_email(email)
    except ValidationError:
        return False
    return True


DB_UNAVAILABLE_ERRORS = (DatabaseError, OperationalError, ProgrammingError)


def _safe_records(model, limit=None):
    try:
        queryset = model.objects.all()
        if limit is not None:
            queryset = queryset[:limit]
        return list(queryset)
    except DB_UNAVAILABLE_ERRORS:
        return []


def _safe_first(model):
    try:
        return model.objects.first()
    except DB_UNAVAILABLE_ERRORS:
        return None


def _database_unavailable_message(request):
    messages.error(
        request,
        'Inquiry storage is not configured yet. Please email or WhatsApp us directly.',
    )


def home(request):
    products = _safe_records(Product, limit=4)
    gallery = _safe_records(Gallery, limit=6)
    return render(request, 'home.html', {
        'products': products,
        'gallery': gallery,
    })


def about(request):
    company = _safe_first(Company)
    return render(request, 'about.html', {'company': company})


def manufacturing(request):
    data = _safe_records(Manufacturing)
    return render(request, 'manufacturing.html', {'data': data})


def products(request):
    products = _safe_records(Product)
    return render(request, 'products.html', {
        'products': products,
        'fabric_catalog': FABRIC_CATALOG,
    })


def gallery(request):
    images = _safe_records(Gallery)
    return render(request, 'gallery.html', {'images': images})


def contact(request):
    selected_subject = request.GET.get('type', '')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company = request.POST.get('company', '').strip()
        subject = request.POST.get('subject', '').strip()
        quantity = request.POST.get('moq', '').strip()
        message = request.POST.get('message', '').strip()
        consent = request.POST.get('consent') == 'on'
        selected_subject = subject

        if not name or not email or not message:
            messages.error(request, 'Please complete your name, email, and message.')
        elif not _is_valid_email(email):
            messages.error(request, 'Please enter a valid email address.')
        elif not consent:
            messages.error(request, 'Please confirm consent so we can contact you.')
        else:
            try:
                Contact.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    company=company,
                    subject=subject,
                    quantity=quantity,
                    message=message,
                    consent=True,
                )
            except DB_UNAVAILABLE_ERRORS:
                _database_unavailable_message(request)
            else:
                messages.success(request, 'Inquiry submitted successfully. Our team will respond within 24 hours.')
                return redirect('contact')

    return render(request, 'contact.html', {
        'selected_subject': selected_subject,
    })


def sample_request(request, fabric):
    fabric_info = FABRIC_CATALOG.get(fabric, {
        'name': fabric.replace('-', ' ').title(),
        'category': 'Custom',
        'image': 'images/p3.jpg',
        'description': 'Tell us what you need and the team will prepare the right fabric recommendation.',
    })

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company = request.POST.get('company', '').strip()
        quantity = request.POST.get('quantity', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not phone:
            messages.error(request, 'Please add your name, email, and phone number.')
        elif not _is_valid_email(email):
            messages.error(request, 'Please enter a valid email address.')
        else:
            try:
                Inquiry.objects.create(
                    fabric_name=fabric_info['name'],
                    customer_name=name,
                    email=email,
                    phone=phone,
                    company=company,
                    quantity=quantity,
                    message=message or f"Sample request for {fabric_info['name']}.",
                )
            except DB_UNAVAILABLE_ERRORS:
                _database_unavailable_message(request)
            else:
                messages.success(request, f"Sample request for {fabric_info['name']} submitted successfully.")
                return redirect('products')

    return render(request, 'inquiry.html', {
        'fabric': fabric_info,
        'fabric_slug': fabric,
    })


def inquiry(request, id):
    try:
        product = get_object_or_404(Product, id=id)
    except DB_UNAVAILABLE_ERRORS:
        messages.error(request, 'Product inquiry storage is not configured yet.')
        return redirect('products')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        quantity = request.POST.get('quantity', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not phone:
            messages.error(request, 'Please add your name, email, and phone number.')
        elif not _is_valid_email(email):
            messages.error(request, 'Please enter a valid email address.')
        else:
            try:
                Inquiry.objects.create(
                    product=product,
                    fabric_name=product.name,
                    customer_name=name,
                    email=email,
                    phone=phone,
                    quantity=quantity,
                    message=message,
                )
            except DB_UNAVAILABLE_ERRORS:
                _database_unavailable_message(request)
            else:
                messages.success(request, 'Inquiry submitted successfully.')
                return redirect('products')

    return render(request, 'inquiry.html', {
        'product': product,
        'fabric': {
            'name': product.name,
            'category': product.category,
            'description': product.description,
            'image_url': product.image.url,
        },
    })


def newsletter_signup(request):
    if request.method != 'POST':
        return redirect('home')

    email = request.POST.get('email', '').strip()
    next_url = request.POST.get('next') or reverse('home')
    if not next_url.startswith('/'):
        next_url = reverse('home')

    if not _is_valid_email(email):
        messages.error(request, 'Please enter a valid email for newsletter updates.')
        return redirect(next_url)

    try:
        _, created = Newsletter.objects.get_or_create(email=email)
    except DB_UNAVAILABLE_ERRORS:
        _database_unavailable_message(request)
        return redirect(next_url)

    if created:
        messages.success(request, 'Newsletter signup complete. You will receive DharmaFab updates.')
    else:
        messages.info(request, 'You are already on the DharmaFab newsletter list.')
    return redirect(next_url)


def legal_page(request, page):
    if page not in {'privacy', 'terms'}:
        return redirect('home')
    return render(request, 'legal.html', {'page': page})


def factory_visit(request):
    return redirect(f"{reverse('contact')}?type=visit")


@login_required
def user_dashboard(request):
    inquiries = Inquiry.objects.filter(email=request.user.email).order_by('-created_at')
    if not inquiries.exists():
        inquiries = Inquiry.objects.filter(customer_name__iexact=request.user.username).order_by('-created_at')
    return render(request, 'dashboard/user_dashboard.html', {
        'inquiries': inquiries,
    })


def user_login(request):
    if request.method == 'POST':
        try:
            user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
            )
        except DB_UNAVAILABLE_ERRORS:
            messages.error(request, 'Dashboard database is not configured yet.')
            user = None
        if user:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    contacts_qs = Contact.objects.all().order_by('-created_at')
    inquiries_qs = Inquiry.objects.all().order_by('-created_at')

    combined_messages = []
    for c in contacts_qs[:20]:
        combined_messages.append({
            'name': c.name,
            'email': c.email,
            'message': c.message,
            'is_read': c.is_read,
            'subject': c.subject or 'General Inquiry',
            'created_at': c.created_at,
        })
    for i in inquiries_qs[:20]:
        combined_messages.append({
            'name': i.customer_name,
            'email': i.email,
            'message': i.message,
            'is_read': False,
            'subject': f"Sample Request: {i.fabric_name}" if i.fabric_name else "Sample Request",
            'created_at': i.created_at,
        })
    combined_messages.sort(key=lambda x: x['created_at'], reverse=True)

    # Chart data: last 6 months
    chart_labels = []
    chart_data = []
    now = timezone.now()
    for i in range(5, -1, -1):
        target_month = (now.month - 1 - i) % 12 + 1
        target_year = now.year + ((now.month - 1 - i) // 12)
        month_name = calendar.month_name[target_month][:3]
        chart_labels.append(f"{month_name} {target_year}")
        
        c_count = Contact.objects.filter(created_at__year=target_year, created_at__month=target_month).count()
        i_count = Inquiry.objects.filter(created_at__year=target_year, created_at__month=target_month).count()
        chart_data.append(c_count + i_count)

    context = {
        'total_products': Product.objects.count(),
        'total_contacts': contacts_qs.count(),
        'total_inquiries': inquiries_qs.count(),
        'total_manufacturing': Manufacturing.objects.count(),
        'total_newsletter': Newsletter.objects.count(),
        'inquiries': inquiries_qs[:5],
        'contacts': combined_messages[:20],
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
