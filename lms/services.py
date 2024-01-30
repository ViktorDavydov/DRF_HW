import stripe
from django.conf import settings

from lms.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_session(serializer: Payment):
    course_title = serializer.paid_course.title
    product = stripe.Product.create(name=course_title)
    price = stripe.Price.create(
        unit_amount=serializer.paid_course.price * 100,
        currency='rub',
        product=product.id,
    )
    session = stripe.checkout.Session.create(
        success_url='https://example.com/success',
        line_items=[
            {
                'price': price.id,
                'quantity': 1,
            }
        ],
        mode='payment',
        customer_email=serializer.user.email
    )
    print(session.__dict__)
    return session


def retrieve_session(session):
    return stripe.checkout.Session.retrieve(session)
