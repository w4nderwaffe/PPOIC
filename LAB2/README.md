# README: Postal Office System (Postal OOP)

- Classes: 63
- Fields: 175
- Unique behaviors: 141
- Associations: 47
- Exceptions: 12

## Exceptions (12)
All custom exceptions are located in the `postal_oop/exceptions` package, each in its own class file.

- DuplicateTrackingError — дубликат трекинг-номера
- InsufficientPostageError — недостаточная оплата пересылки
- LockerOccupiedError — ячейка постамата уже занята
- OversizeError — превышены габариты отправления
- OverweightError — превышен допустимый вес
- PaymentDeclinedError — платёж отклонён
- ProhibitedContentError — запрещённое вложение в посылке
- RoutingError — ошибка маршрутизации отправления
- SortingError — ошибка сортировки на сортировочном центре
- TrackingNotFoundError — трекинг-номер не найден
- AddressInvalidError — некорректный почтовый адрес
- DeliveryAttemptFailedError — неудачная попытка доставки

## Classes
Format: `Class Fields Methods → Associations (used classes)`

### Core domain entities

Customer 3 3 → Person
- Fields:
  - loyalty_points — поле доменной модели
  - preferred_office_id — поле доменной модели
  - preferences — поле доменной модели
- Methods:
  - add_points() — добавление связанных данных
  - set_preference() — бизнес-операция класса
  - prefers_office() — бизнес-операция класса

InsurancePlan 4 2
- Fields:
  - code — поле доменной модели
  - max_cover_value — поле доменной модели
  - price_percent — поле доменной модели
  - min_price — поле доменной модели
- Methods:
  - premium() — бизнес-операция класса
  - can_cover() — бизнес-операция класса

Person 4 2
- Fields:
  - full_name — полное имя
  - id_number — поле доменной модели
  - phone — номер телефона
  - email — email-адрес
- Methods:
  - short_name() — бизнес-операция класса
  - has_contact() — бизнес-операция класса

PostalAddress 6 4
- Fields:
  - street — поле доменной модели
  - house — поле доменной модели
  - postal_code — поле доменной модели
  - city — поле доменной модели
  - country — поле доменной модели
  - apartment — поле доменной модели
- Methods:
  - formatted() — бизнес-операция класса
  - validate() — валидация данных
  - same_city() — бизнес-операция класса
  - region_hint() — бизнес-операция класса

Postbox 5 4 → PostalAddress
- Fields:
  - id — идентификатор записи
  - address — почтовой адрес
  - max_items — поле доменной модели
  - max_weight_kg — поле доменной модели
  - _items_weights — поле доменной модели
- Methods:
  - can_accept() — бизнес-операция класса
  - receive_item() — бизнес-операция класса
  - pickup() — бизнес-операция класса
  - load_factor() — бизнес-операция класса

Postmark 4 3
- Fields:
  - office_id — поле доменной модели
  - country — поле доменной модели
  - code — поле доменной модели
  - stamped_at — поле доменной модели
- Methods:
  - to_string() — бизнес-операция класса
  - is_older_than() — бизнес-операция класса
  - apply_to_text() — бизнес-операция класса

Stamp 5 3
- Fields:
  - code — поле доменной модели
  - face_value — поле доменной модели
  - country — поле доменной модели
  - issued_on — поле доменной модели
  - cancelled — поле доменной модели
- Methods:
  - cancel() — бизнес-операция класса
  - is_valid_for_country() — бизнес-операция класса
  - value_left() — бизнес-операция класса

Tariff 7 2
- Fields:
  - code — поле доменной модели
  - name — название/имя
  - base_price — поле доменной модели
  - price_per_kg — поле доменной модели
  - included_weight_kg — поле доменной модели
  - zone — поле доменной модели
  - priority — приоритет обработки/отправления
- Methods:
  - estimate() — бизнес-операция класса
  - is_international() — бизнес-операция класса

WeightBand 2 1
- Fields:
  - max_weight_kg — поле доменной модели
  - label — поле доменной модели
- Methods:
  - fits() — бизнес-операция класса

### Domain & config

DNSRecord 2 2
- Fields:
  - key — поле доменной модели
  - value — поле доменной модели
- Methods:
  - as_tuple() — бизнес-операция класса
  - matches() — бизнес-операция класса

Domain 5 6 → DNSRecord
- Fields:
  - code — поле доменной модели
  - name — название/имя
  - offices — поле доменной модели
  - centers — поле доменной модели
  - records — поле доменной модели
- Methods:
  - add_office() — добавление связанных данных
  - add_center() — добавление связанных данных
  - add_record() — добавление связанных данных
  - has_office() — бизнес-операция класса
  - has_center() — бизнес-операция класса
  - find_records() — бизнес-операция класса

ServerConfig 3 4 → Domain
- Fields:
  - domain — поле доменной модели
  - hub_id — поле доменной модели
  - allowed_zones — поле доменной модели
- Methods:
  - is_local_route() — бизнес-операция класса
  - zone_for() — бизнес-операция класса
  - knows_office() — бизнес-операция класса
  - hub() — бизнес-операция класса

### Engines

PricingEngine 3 3 → InsurancePlan, PostalItem, Tariff, WeightBand
- Fields:
  - tariffs — поле доменной модели
  - bands — поле доменной модели
  - default_insurance — поле доменной модели
- Methods:
  - pick_tariff() — бизнес-операция класса
  - in_band() — бизнес-операция класса
  - calculate() — расчётное действие

RoutingEngine 0 1 → PostalAddress, Route
- Methods:
  - plan() — бизнес-операция класса

SortingEngine 0 2 → PostalItem
- Methods:
  - choose_center() — бизнес-операция класса
  - barcode_ok() — бизнес-операция класса

### Postal items

FragileParcel 1 2 → Parcel
- Fields:
  - fragile_fee — поле доменной модели
- Methods:
  - total_price() — бизнес-операция класса
  - handling_note() — бизнес-операция класса

InsuredParcel 1 3 → AttachmentList, Parcel
- Fields:
  - attachment — поле доменной модели
- Methods:
  - require_insurance() — бизнес-операция класса
  - total_price() — бизнес-операция класса
  - claim_value() — бизнес-операция класса

Letter 0 1 → PostalItem
- Methods:
  - service_limits() — бизнес-операция класса

OversizedParcel 1 2 → Parcel
- Fields:
  - oversize_fee — поле доменной модели
- Methods:
  - service_limits() — бизнес-операция класса
  - total_price() — бизнес-операция класса

Parcel 0 1 → PostalItem
- Methods:
  - service_limits() — бизнес-операция класса

PostalItem 10 6 → InsurancePlan, PostalAddress, Postmark, Tariff
- Fields:
  - tracking_id — трекинг-идентификатор
  - sender — отправитель
  - recipient — получатель
  - weight_kg — вес в килограммах
  - size_cm — поле доменной модели
  - stamps_value — поле доменной модели
  - tariff — тариф для расчёта стоимости
  - insurance_plan — поле доменной модели
  - postmarks — поле доменной модели
  - declared_value — поле доменной модели
- Methods:
  - service_limits() — бизнес-операция класса
  - check_limits() — бизнес-операция класса
  - add_postmark() — добавление связанных данных
  - base_price() — бизнес-операция класса
  - total_price() — бизнес-операция класса
  - verify_postage() — валидация данных

Postcard 0 1 → PostalItem
- Methods:
  - service_limits() — бизнес-операция класса

ProhibitedItemCheck 1 1 → AttachmentList
- Fields:
  - prohibited_keywords — поле доменной модели
- Methods:
  - scan() — бизнес-операция класса

RegisteredLetter 1 1 → Letter
- Fields:
  - registration_fee — поле доменной модели
- Methods:
  - total_price() — бизнес-операция класса

SmallPackage 0 1 → Parcel
- Methods:
  - service_limits() — бизнес-операция класса

AttachmentList 3 3 → CustomsDeclaration
- Fields:
  - documents — поле доменной модели
  - customs — поле доменной модели
  - items — список вложений/отправлений
- Methods:
  - add() — добавление связанных данных
  - total_weight() — бизнес-операция класса
  - keywords() — бизнес-операция класса

CODParcel 1 2 → Parcel
- Fields:
  - cod_amount — поле доменной модели
- Methods:
  - requires_cod() — бизнес-операция класса
  - collect_cod() — бизнес-операция класса

CustomsDeclaration 5 2
- Fields:
  - content_description — поле доменной модели
  - value_eur — поле доменной модели
  - country_of_origin — поле доменной модели
  - hs_code — поле доменной модели
  - is_document — поле доменной модели
- Methods:
  - requires_declaration() — бизнес-операция класса
  - estimate_duties() — бизнес-операция класса

### Logistics & transport

Courier 7 6 → PostalAddress, TransportUnit
- Fields:
  - id — идентификатор записи
  - unit — поле доменной модели
  - name — название/имя
  - full_name — полное имя
  - planned_stops — поле доменной модели
  - current_load_kg — поле доменной модели
  - _cursor — поле доменной модели
- Methods:
  - assign_route() — бизнес-операция класса
  - next_stop() — бизнес-операция класса
  - advance() — бизнес-операция класса
  - load() — бизнес-операция класса
  - unload() — бизнес-операция класса
  - attempt_delivery() — бизнес-операция класса

CourierRoutePlan 2 3 → PostalAddress
- Fields:
  - courier_id — поле доменной модели
  - stops — поле доменной модели
- Methods:
  - add_stop() — добавление связанных данных
  - next_after() — бизнес-операция класса
  - total_stops() — бизнес-операция класса

Locker 4 5 → PostalAddress
- Fields:
  - id — идентификатор записи
  - location — поле доменной модели
  - max_weight_per_cell_kg — поле доменной модели
  - cells — поле доменной модели
- Methods:
  - add_cell() — добавление связанных данных
  - is_free() — бизнес-операция класса
  - reserve() — бизнес-операция класса
  - put() — бизнес-операция класса
  - pickup() — бизнес-операция класса

PostOffice 5 5 → PostalAddress, PostalItem
- Fields:
  - id — идентификатор записи
  - address — почтовой адрес
  - services — поле доменной модели
  - cash_balance — поле доменной модели
  - queue_counter — поле доменной модели
- Methods:
  - issue_queue_ticket() — бизнес-операция класса
  - accept_item() — бизнес-операция класса
  - deliver_item() — бизнес-операция класса
  - receive_payment() — бизнес-операция класса
  - payout_cod() — бизнес-операция класса

Route 3 2
- Fields:
  - id — идентификатор записи
  - nodes — поле доменной модели
  - zone — поле доменной модели
- Methods:
  - next_after() — бизнес-операция класса
  - total_hops() — бизнес-операция класса

SortingCenter 4 5 → PostalItem
- Fields:
  - id — идентификатор записи
  - name — название/имя
  - capacity — поле доменной модели
  - queue — поле доменной модели
- Methods:
  - enqueue() — бизнес-операция класса
  - dequeue() — бизнес-операция класса
  - route_hint() — бизнес-операция класса
  - has_item() — бизнес-операция класса
  - queue_size() — бизнес-операция класса

TrainCar 4 1 → TransportUnit
- Fields:
  - id — идентификатор записи
  - number — поле доменной модели
  - unit — поле доменной модели
  - gauge_mm — поле доменной модели
- Methods:
  - axle_load_ok() — бизнес-операция класса

TransportUnit 5 3
- Fields:
  - id — идентификатор записи
  - kind — поле доменной модели
  - max_load_kg — поле доменной модели
  - current_load_kg — поле доменной модели
  - location_node_id — поле доменной модели
- Methods:
  - can_load() — бизнес-операция класса
  - load() — бизнес-операция класса
  - unload() — бизнес-операция класса

Truck 5 1 → TransportUnit
- Fields:
  - id — идентификатор записи
  - plate — поле доменной модели
  - unit — поле доменной модели
  - axle_count — поле доменной модели
  - refrigerated — поле доменной модели
- Methods:
  - fuel_needed() — бизнес-операция класса

Van 4 1 → TransportUnit
- Fields:
  - id — идентификатор записи
  - plate — поле доменной модели
  - unit — поле доменной модели
  - doors — поле доменной модели
- Methods:
  - city_efficiency() — бизнес-операция класса

AirFreight 4 1 → TransportUnit
- Fields:
  - id — идентификатор записи
  - flight — поле доменной модели
  - unit — поле доменной модели
  - icao — поле доменной модели
- Methods:
  - iata_label() — бизнес-операция класса

### Notifications

EmailNotifier 1 1
- Fields:
  - from_addr — поле доменной модели
- Methods:
  - send_status_update() — отправка/инициация операции

PushNotifier 1 1
- Fields:
  - provider — поле доменной модели
- Methods:
  - send_status_update() — отправка/инициация операции

SMSNotifier 1 1
- Fields:
  - sender_id — поле доменной модели
- Methods:
  - send_status_update() — отправка/инициация операции

### Operations & tracking

CashRegister 4 4
- Fields:
  - id — идентификатор записи
  - opened — поле доменной модели
  - balance — поле доменной модели
  - payments_log — поле доменной модели
- Methods:
  - open_shift() — бизнес-операция класса
  - close_shift() — бизнес-операция класса
  - accept_payment() — бизнес-операция класса
  - refund() — бизнес-операция класса

Manifest 6 6 → Shipment
- Fields:
  - id — идентификатор записи
  - route_id — поле доменной модели
  - shipments — поле доменной модели
  - shipment_id — поле доменной модели
  - _entries — поле доменной модели
  - _weight_kg — поле доменной модели
- Methods:
  - add() — добавление связанных данных
  - add_entry() — добавление связанных данных
  - total_items() — бизнес-операция класса
  - total_weight() — бизнес-операция класса
  - ids() — бизнес-операция класса
  - has_tracking() — бизнес-операция класса

Payment 5 2
- Fields:
  - id — идентификатор записи
  - amount — сумма операции
  - currency — поле доменной модели
  - method — поле доменной модели
  - approved — поле доменной модели
- Methods:
  - authorize() — бизнес-операция класса
  - is_cash() — бизнес-операция класса

QueueTicket 4 3
- Fields:
  - office_id — поле доменной модели
  - number — поле доменной модели
  - issued_at — поле доменной модели
  - served_at — поле доменной модели
- Methods:
  - code() — бизнес-операция класса
  - mark_served() — изменение статуса/пометка
  - wait_time_min() — бизнес-операция класса

Receipt 4 3
- Fields:
  - id — идентификатор записи
  - payment_id — поле доменной модели
  - items — список вложений/отправлений
  - footer_note — поле доменной модели
- Methods:
  - add_item() — добавление связанных данных
  - total() — бизнес-операция класса
  - render_text() — бизнес-операция класса

Shipment 7 3 → TransportUnit
- Fields:
  - id — идентификатор записи
  - route_id — поле доменной модели
  - unit — поле доменной модели
  - item_ids — поле доменной модели
  - total_weight_kg — поле доменной модели
  - departed — поле доменной модели
  - arrived — поле доменной модели
- Methods:
  - add_item() — добавление связанных данных
  - depart() — бизнес-операция класса
  - arrive() — бизнес-операция класса

TrackingEvent 5 2
- Fields:
  - tracking_id — трекинг-идентификатор
  - status — текущий статус
  - location_node_id — поле доменной модели
  - timestamp — поле доменной модели
  - note — поле доменной модели
- Methods:
  - as_dict() — бизнес-операция класса
  - is_final() — бизнес-операция класса

TrackingId 1 2
- Fields:
  - code — поле доменной модели
- Methods:
  - new() — бизнес-операция класса
  - normalized() — бизнес-операция класса

### Services

PostalService 12 12 → CashRegister, Courier, EmailNotifier, PostOffice, PostalItem, PricingEngine, PushNotifier, Receipt, Route, RoutingEngine, SMSNotifier, ServerConfig, SortingCenter, SortingEngine, TrackingEvent
- Fields:
  - config — поле доменной модели
  - pricing — поле доменной модели
  - routing — поле доменной модели
  - sorting — поле доменной модели
  - offices — поле доменной модели
  - centers — поле доменной модели
  - registers — поле доменной модели
  - track_events — поле доменной модели
  - registry_items — поле доменной модели
  - sms — поле доменной модели
  - email — email-адрес
  - push — поле доменной модели
- Methods:
  - register_office() — регистрация сущности/операции
  - register_center() — регистрация сущности/операции
  - add_event() — добавление связанных данных
  - history() — бизнес-операция класса
  - register_item() — регистрация сущности/операции
  - quote() — бизнес-операция класса
  - accept_at_office() — бизнес-операция класса
  - plan_route() — бизнес-операция класса
  - handover_to_center() — бизнес-операция класса
  - deliver_by_courier() — бизнес-операция класса
  - notify_all() — бизнес-операция класса
  - issue_receipt() — бизнес-операция класса

## Associations (55)
Format: `ClassA → ClassB (краткое пояснение, файл: путь)`

- AirFreight → TransportUnit (AirFreight использует TransportUnit в полях или методах; файл: postal_oop/logistics/AirFreight.py)
- AttachmentList → CustomsDeclaration (AttachmentList использует CustomsDeclaration в полях или методах; файл: postal_oop/items/AttachmentList.py)
- CODParcel → Parcel (CODParcel работает с посылкой Parcel; файл: postal_oop/items/CODParcel.py)
- Courier → PostalAddress (Courier использует PostalAddress для работы с адресами; файл: postal_oop/logistics/Courier.py)
- Courier → TransportUnit (Courier использует TransportUnit в полях или методах; файл: postal_oop/logistics/Courier.py)
- CourierRoutePlan → PostalAddress (CourierRoutePlan использует PostalAddress для работы с адресами; файл: postal_oop/logistics/CourierRoutePlan.py)
- Customer → Person (Customer наследует Person (клиент — частный случай персоны); файл: postal_oop/core/Customer.py)
- Domain → DNSRecord (Domain использует DNSRecord в полях или методах; файл: postal_oop/domain/Domain.py)
- FragileParcel → Parcel (FragileParcel работает с посылкой Parcel; файл: postal_oop/items/FragileParcel.py)
- InsuredParcel → AttachmentList (InsuredParcel использует AttachmentList в полях или методах; файл: postal_oop/items/InsuredParcel.py)
- InsuredParcel → Parcel (InsuredParcel работает с посылкой Parcel; файл: postal_oop/items/InsuredParcel.py)
- Letter → PostalItem (Letter специализация или обработка базового PostalItem; файл: postal_oop/items/Letter.py)
- Locker → PostalAddress (Locker использует PostalAddress для работы с адресами; файл: postal_oop/logistics/Locker.py)
- Manifest → Shipment (Manifest использует Shipment в полях или методах; файл: postal_oop/operations/Manifest.py)
- OversizedParcel → Parcel (OversizedParcel работает с посылкой Parcel; файл: postal_oop/items/OversizedParcel.py)
- Parcel → PostalItem (Parcel специализация или обработка базового PostalItem; файл: postal_oop/items/Parcel.py)
- PostOffice → PostalAddress (PostOffice использует PostalAddress для работы с адресами; файл: postal_oop/logistics/PostOffice.py)
- PostOffice → PostalItem (PostOffice специализация или обработка базового PostalItem; файл: postal_oop/logistics/PostOffice.py)
- PostalItem → InsurancePlan (PostalItem использует InsurancePlan в полях или методах; файл: postal_oop/items/PostalItem.py)
- PostalItem → PostalAddress (PostalItem использует PostalAddress для работы с адресами; файл: postal_oop/items/PostalItem.py)
- PostalItem → Postmark (PostalItem использует Postmark в полях или методах; файл: postal_oop/items/PostalItem.py)
- PostalItem → Tariff (PostalItem использует Tariff в полях или методах; файл: postal_oop/items/PostalItem.py)

## Summary

The Postal Office System (Postal OOP) implements a full domain model for postal operations based on core entities, postal items, logistics, tariffs, operations and services. 
This README describes the real class structure of the project: exceptions, classes grouped by packages with short Russian explanations for fields and methods, and 55 sample associations between them, with Russian explanations and file paths that match the actual architecture.


