# Part 1: Application Selection & Analysis

## Application: FoodHub — Online Food Delivery Platform

### Purpose

FoodHub is a hypothetical food-delivery platform that connects customers with local restaurants and couriers. Customers use a responsive website or mobile application to discover restaurants, browse menus, customize items, pay, follow an order, and rate the experience. Restaurants use an operational dashboard to manage menus, availability, preparation time, and incoming orders. Couriers receive delivery assignments through a mobile application, navigate to pickup and delivery locations, and update order status. The platform earns service and delivery fees, so an accurate and reliable order flow protects both customer trust and business revenue.

### Target Users

- **Customers** search for food, save addresses, build carts, pay, track deliveries, and contact support.
- **Restaurant staff** publish menu availability, accept or reject orders, set preparation times, and manage substitutions.
- **Couriers** accept assignments, share location during active deliveries, and record pickup and delivery events.
- **Support staff** investigate cancellations, late deliveries, missing items, refunds, and payment disputes.

### Key Features

1. Registration, authentication, recovery, profiles, and saved addresses.
2. Restaurant search with cuisine, rating, price, location, and availability filters.
3. Menu browsing with modifiers, allergens, inventory status, and cart management.
4. Checkout that calculates items, taxes, delivery fees, promotions, tips, and final total.
5. Tokenized card or wallet payment and an authoritative receipt.
6. Restaurant acceptance, substitutions, estimated preparation time, and order management.
7. Courier assignment, live status, location sharing, and delivery confirmation.
8. Cancellations, refunds, ratings, reviews, support, and notifications.

### Technology Stack Assumptions

FoodHub is a web application plus iOS and Android clients. A component-based frontend communicates with HTTPS REST APIs. Backend services use a relational database for orders and payments, Redis for sessions and carts, and asynchronous queues for notifications and courier events. Maps, payments, notifications, and identity verification are third-party integrations. These boundaries make contract, timeout, retry, privacy, and event-ordering tests important.

### Critical Functions

Checkout is the highest-risk path: selected items must be available; the price, fees, tax, tip, and promotion must be correct; payment must be authorized once; and the restaurant must receive exactly one order. Authentication protects addresses, history, and payment tokens. Accurate order status, courier assignment, location permission, refund authorization, and availability synchronization are also critical because defects can cause financial loss, privacy exposure, unsafe handoffs, or an order that cannot be fulfilled.
