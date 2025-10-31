# Internet Shop — Class Catalogue

---

## 1. Classes (Attributes • Methods → Associations)

### catalog/
**Product**  
- *Attributes:* id, name, slug, description, price, currency, images[], category, stock, rating  
- *Methods:* apply_discount(), change_price(), is_in_stock(), serialize()  
- *Associations:* Category, Image, Review, Price

**Category**  
- *Attributes:* id, name, slug, parent?, children[]  
- *Methods:* add_child(), ancestors(), path()  
- *Associations:* Product (1—*), Category (self)

**Price**  
- *Attributes:* amount, currency, fraction_digits  
- *Methods:* as_float(), with_tax(rate), format()  
- *Associations:* Product, Currency

**Image**  
- *Attributes:* url, alt, width, height, is_primary  
- *Methods:* thumbnail(), optimize()  
- *Associations:* Product

**Review**  
- *Attributes:* id, user, product, rating, text, created_at  
- *Methods:* edit(), moderate(), stars()  
- *Associations:* User, Product

---

### users/
**User**  
- *Attributes:* id, email, password_hash, name, phone, role  
- *Methods:* check_password(), can(action), profile()  
- *Associations:* Address, Order, Review

**Address**  
- *Attributes:* id, user, country, city, street, house, apartment, postal_code  
- *Methods:* normalize(), to_string()  
- *Associations:* User, Order

---

### cart/
**Cart**  
- *Attributes:* id, user?, items[], total, currency  
- *Methods:* add(product, qty), remove(product), clear(), recalc()  
- *Associations:* CartItem, Product, User, Coupon

**CartItem**  
- *Attributes:* product, qty, price, amount  
- *Methods:* subtotal(), change_qty()  
- *Associations:* Product, Cart

**Coupon**  
- *Attributes:* code, percent?, amount?, valid_from, valid_to, min_total  
- *Methods:* is_valid(now, cart), apply(cart)  
- *Associations:* Cart, Order

---

### orders/
**Order**  
- *Attributes:* id, user, items[], status, total, currency, created_at, paid_at?  
- *Methods:* confirm(), pay(), cancel(), refund(), recalc()  
- *Associations:* OrderItem, User, Payment, Shipment, Address, Coupon

**OrderItem**  
- *Attributes:* product, qty, price, amount  
- *Methods:* subtotal()  
- *Associations:* Product, Order

**Shipment**  
- *Attributes:* id, order, carrier, tracking_code, status  
- *Methods:* dispatch(), in_transit(), delivered()  
- *Associations:* Order, Carrier

**Carrier**  
- *Attributes:* id, name, service_level  
- *Methods:* quote(order), track(code)  
- *Associations:* Shipment

---

### payments/
**Payment**  
- *Attributes:* id, order, method, amount, currency, status, gateway_id?  
- *Methods:* authorize(), capture(), void(), refund()  
- *Associations:* Order, Invoice, Gateway

**Invoice**  
- *Attributes:* id, order, number, lines[], total, issued_at  
- *Methods:* add_line(), totalize(), render()  
- *Associations:* Order, Payment

**Gateway**  
- *Attributes:* name, config  
- *Methods:* charge(amount, currency), refund(tx_id)  
- *Associations:* Payment

---

### catalog/filters/
**Filter**  
- *Attributes:* key, op, value  
- *Methods:* apply(queryset)  
- *Associations:* Product

**Sorter**  
- *Attributes:* key, direction  
- *Methods:* apply(queryset)  
- *Associations:* Product

---

### admin/ (service layer)
**AdminService**  
- *Attributes:* repo(s)  
- *Methods:* create_product(), update_product(), delete_product(), ban_user()  
- *Associations:* Product, User, Category

**CatalogService**  
- *Attributes:* repo(s)  
- *Methods:* list_products(), product_details(), related(), reviews_for(product)  
- *Associations:* Product, Category, Review

**CheckoutService**  
- *Attributes:* repo(s)  
- *Methods:* start_checkout(), place_order(), pay(order, method)  
- *Associations:* Cart, Order, Payment, User

**NotificationService**  
- *Attributes:* mailer, sms, push  
- *Methods:* order_confirmed(order), payment_captured(order), shipped(order)  
- *Associations:* Order, User

---

## 2. Exceptions (12)

1. ProductNotFoundError — product id not found.  
2. OutOfStockError — requested quantity exceeds inventory.  
3. CartEmptyError — operation requires non‑empty shopping cart.  
4. OrderNotFoundError — order id not present in registry.  
5. PaymentDeclinedError — payment gateway refused the charge.  
6. InvalidCouponError — coupon not applicable or expired.  
7. UnauthorizedOperationError — user not allowed to perform this action.  
8. AddressInvalidError — shipping address invalid or incomplete.  
9. InventorySyncError — inventory state cannot be synchronized.  
10. DuplicateEmailError — user email already exists.  
11. RefundFailedError — refund operation failed in gateway.  
12. NotificationFailedError — email/SMS/push notification failed.

---

## Results

Fields: 112  
Behaviors: 102  
Associations: 30  
Exceptions: 12  
Classes: 49

