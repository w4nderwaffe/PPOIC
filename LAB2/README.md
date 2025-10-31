
# Postal OOP System — Class Catalogue

---

## 1. Classes (Attributes • Methods → Associations)

### core/

**PostalAddress**  
- *Attributes:* street, house, postal_code, city, country, apartment?  
- *Methods:* validation, normalization, string representation  
- *Associations:* used by all PostalItem, PostOffice  

**Tariff**  
- *Attributes:* code, name, base_price, price_per_kg, included_weight_kg, zone, priority  
- *Methods:* price(weight), zone checks  
- *Associations:* PostalItem, PricingEngine  

**WeightBand**  
- *Attributes:* max_weight_kg, label  
- *Methods:* fits(weight)  
- *Associations:* PricingEngine  

**InsurancePlan**  
- *Attributes:* limit, rate  
- *Methods:* premium(value)  
- *Associations:* PostalItem (insured types)  

**Person / Customer**  
- *Attributes:* name, phone, email  
- *Methods:* getters, validation  
- *Associations:* notifications, PostalItem  

**Postbox**  
- *Attributes:* id, address, capacity  
- *Methods:* drop(item), pickup()  
- *Associations:* logistics  

**Stamp**  
- *Attributes:* face_value, currency  
- *Methods:* to_string()  
- *Associations:* PostalItem  

---

### items/

**PostalItem (abstract)**  
- *Attributes:* tracking_id, sender, recipient, weight_kg, size_cm, stamps_value, tariff, insurance_plan?, declared_value, postmarks[]  
- *Methods:* service_limits(), check_limits(), base_price(), total_price()  
- *Associations:* PostalAddress, Tariff, InsurancePlan  

**Letter**  
- *Attributes:* base attributes, envelope size limits  
- *Methods:* override service_limits()  
- *Associations:* Tariff  

**RegisteredLetter**  
- *Attributes:* base + registration_fee  
- *Methods:* override total_price()  
- *Associations:* Tariff  

**Parcel**  
- *Attributes:* base + parcel limits (weight, dimensions)  
- *Methods:* override service_limits()  
- *Associations:* Tariff  

**InsuredParcel**  
- *Attributes:* base + insurance_plan  
- *Methods:* override total_price() to include insurance  
- *Associations:* Tariff, InsurancePlan  

**Postcard**  
- *Attributes:* simplified weight/size  
- *Methods:* base_price()  
- *Associations:* Tariff  

---

### operations/

**TrackingId**  
- *Attributes:* prefix, serial, checksum  
- *Methods:* new(), normalized()  
- *Associations:* PostalItem  

**TrackingEvent**  
- *Attributes:* tracking_id, status, location_node_id, timestamp, note?  
- *Methods:* to_string()  
- *Associations:* TrackingId  

**Manifest**  
- *Attributes:* id, items, created_at  
- *Methods:* add(), remove(), count()  
- *Associations:* TrackingId  

**Shipment**  
- *Attributes:* id, source_node, dest_node, manifest  
- *Methods:* load(), seal(), handover()  
- *Associations:* Manifest  

**CashRegister**  
- *Attributes:* id, opened, balance  
- *Methods:* open_shift(), accept_payment(), refund(), close_shift()  
- *Associations:* PostOffice, Receipt  

**QueueTicket**  
- *Attributes:* number, issued_at, channel  
- *Methods:* to_string()  
- *Associations:* PostOffice  

---

### logistics/

**PostOffice**  
- *Attributes:* id, address, services, cash_balance, queue_counter  
- *Methods:* accept_item(), deliver_item(), interact_with_cash_register()  
- *Associations:* PostalAddress, CashRegister  

**SortingCenter**  
- *Attributes:* id, name, capacity, queue  
- *Methods:* accept(), sort()  
- *Associations:* Manifest, Shipment  

**Courier**  
- *Attributes:* id, full_name, unit?  
- *Methods:* deliver(item, recipient_present)  
- *Associations:* Route  

**Route**  
- *Attributes:* id, nodes, zone  
- *Methods:* iterate(), to_string()  
- *Associations:* RoutingEngine, Courier  

---

### services/

**PostalService**  
- *Attributes:* config, pricing, sorting, routing, notifiers  
- *Methods:* register_office(), register_center(), register_item(), quote(), accept_at_office(), handover_to_center(), plan_route(), deliver_by_courier(), issue_receipt(), add_event(), history(), notify_all()  
- *Associations:* ServerConfig, PricingEngine, SortingEngine, RoutingEngine, PostOffice, Courier, TrackingEvent  

**Receipt**  
- *Attributes:* id, office_id, payment_id, lines, total, footer, issued_at  
- *Methods:* to_string(), export()  
- *Associations:* CashRegister  

---

### domain/ & engines/

**Domain**  
- *Attributes:* code, name, records  
- *Methods:* add_office(), add_center(), find_records(), has()  
- *Associations:* PostOffice, SortingCenter  

**ServerConfig**  
- *Attributes:* domain, hub_id, allowed_zones  
- *Methods:* is_local_route(), zone_for()  
- *Associations:* Domain  

**PricingEngine**  
- *Attributes:* tariffs, bands  
- *Methods:* pick_tariff(), quote()  
- *Associations:* Tariff, WeightBand, PostalItem  

**SortingEngine**  
- *Attributes:* policies  
- *Methods:* sort()  
- *Associations:* Manifest  

**RoutingEngine**  
- *Attributes:* policies  
- *Methods:* build_route()  
- *Associations:* Route  

---

### notifications/

**EmailNotifier / SmsNotifier / PushNotifier**  
- *Attributes:* config, credentials  
- *Methods:* notify(contact, text)  
- *Associations:* PostalService  

---

## 2. Exceptions (12)

1. OversizeError — item exceeds allowed dimensions.  
2. TrackingNotFoundError — tracking id not found in history.  
3. AddressInvalidError — invalid or incomplete address.  
4. DuplicateTrackingError — duplicate tracking id.  
5. OfficeNotFoundError — post office not found.  
6. RouteBuildError — cannot construct delivery route.  
7. PaymentError — payment rejected or register closed.  
8. InvalidTariffError — tariff not found for zone/priority.  
9. UnauthorizedOperationError — operation not allowed.  
10. InvalidWeightBandError — item weight not in any band.  
11. ReceiptNotFoundError — receipt id missing in registry.  
12. NotificationFailedError — notification sending failed.  

---

## Results

Classes: 50
Fields: 193  
Behaviors: 175  
Associations: 67  
Exceptions: 12


