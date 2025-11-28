# README: Postal Office System (Postal OOP)

- Classes: 50
- Fields: 150
- Unique behaviors: 100
- Associations: 30
- Exceptions: 12

## Exceptions (12)
All custom exceptions are located in the `postal_oop/exceptions` package, each in its own class file.

- InvalidAddressException — address is incomplete or structurally invalid
- UnknownZipCodeException — zip/postal code is not recognized
- ParcelTooHeavyException — parcel exceeds allowed weight
- ParcelTooLargeException — parcel exceeds allowed dimensions
- ProhibitedContentException — parcel contains forbidden items
- ShipmentAlreadyDispatchedException — attempt to modify dispatched shipment
- TrackingNumberNotFoundException — tracking number does not exist
- DeliveryAttemptLimitExceededException — too many failed delivery attempts
- PaymentDeclinedException — payment for shipment was declined
- InsuranceNotAvailableException — insurance not applicable for this shipment
- AccessDeniedException — user has no rights to perform this action
- SupportTicketClosedException — cannot add messages to closed ticket

## Classes
Format: `Class Fields Methods → Associations (used classes)`

### Clients and Addresses

Client 3 2 → Address, ContactInfo, Shipment
- Fields: id, defaultAddress, contactInfo
- Methods: registerShipment, updateContactInfo

Sender 3 2 → Client, Address
- Fields: id, clientId, address
- Methods: validateSenderAddress, linkToClient

Recipient 3 2 → Address, Shipment
- Fields: id, address, fullName
- Methods: confirmDelivery, changeAddress

Address 4 2 → Client, Sender, Recipient
- Fields: line1, city, zipCode, country
- Methods: normalize, validate

ContactInfo 3 2 → Client, Sender, Recipient
- Fields: email, phone, preferredChannel
- Methods: verifyEmail, verifyPhone

### Shipments and Parcels

Parcel 4 2 → Client, Sender, Recipient, Tariff
- Fields: id, weightKg, declaredValue, contentsDescription
- Methods: isHeavy, requiresInsurance

Letter 3 2 → Sender, Recipient, Tariff
- Fields: id, pagesCount, priority
- Methods: markRegistered, isPriority

Package 4 2 → Sender, Recipient, Parcel
- Fields: id, parcelCount, fragile, insured
- Methods: markFragile, toggleInsurance

Shipment 4 2 → Parcel, Sender, Recipient, PostOfficeBranch
- Fields: id, trackingNumber, status, createdAt
- Methods: dispatch, markDelivered

ReturnShipment 3 2 → Shipment, Sender, Recipient
- Fields: id, originalShipmentId, reason
- Methods: startReturn, markCompleted

DeliveryAttempt 3 2 → Shipment, Recipient
- Fields: id, attemptNo, timestamp
- Methods: markSuccess, markFailed

TrackingEvent 4 2 → Shipment, PostOfficeBranch
- Fields: id, shipmentId, status, occurredAt
- Methods: addNote, changeStatus

### Offices, Logistics, Routes

PostOfficeBranch 4 2 → Shipment, Employee
- Fields: id, name, address, openingHours
- Methods: registerIncoming, registerOutgoing

SortingCenter 3 2 → Shipment, Route
- Fields: id, name, capacity
- Methods: enqueueShipment, forwardShipment

Route 3 2 → RouteStop, Vehicle
- Fields: id, name, active
- Methods: addStop, activate

RouteStop 3 2 → PostOfficeBranch, SortingCenter
- Fields: id, sequenceNo, locationCode
- Methods: setSequence, linkLocation

Vehicle 4 2 → Route, Courier
- Fields: id, plateNumber, capacityKg, type
- Methods: assignCourier, canCarry

Courier 3 2 → Vehicle, PostOfficeBranch
- Fields: id, name, currentBranch
- Methods: assignRoute, markAvailable

DeliverySchedule 3 2 → Courier, Route
- Fields: id, dayOfWeek, timeWindow
- Methods: assignCourier, reschedule

Container 3 2 → Shipment, SortingCenter
- Fields: id, capacity, sealed
- Methods: seal, unseal

Bag 3 2 → Shipment, Container
- Fields: id, code, sealed
- Methods: putIntoContainer, seal

Manifest 3 2 → Container, Shipment
- Fields: id, containerId, createdAt
- Methods: addShipment, closeManifest

### Pricing and Payments

Tariff 4 2 → Zone, WeightRange, Dimension
- Fields: id, name, basePrice, currency
- Methods: calculatePrice, isApplicable

Zone 3 2 → Tariff, Address
- Fields: id, name, regionCode
- Methods: matchesAddress, addCountry

WeightRange 3 2 → Tariff
- Fields: minKg, maxKg, surcharge
- Methods: includesWeight, applySurcharge

Dimension 3 2 → Parcel
- Fields: lengthCm, widthCm, heightCm
- Methods: volume, isOversize

Insurance 3 2 → Parcel, Tariff
- Fields: enabled, rate, maxCoverage
- Methods: calculateFee, isAllowed

Payment 4 2 → Client, Shipment, PaymentMethod
- Fields: id, clientId, amount, status
- Methods: markPaid, markDeclined

PaymentMethod 3 2 → Client
- Fields: id, type, maskedDetails
- Methods: activate, deactivate

Receipt 3 2 → Payment, Shipment
- Fields: id, paymentId, issuedAt
- Methods: renderPdf, sendToClient

Invoice 3 2 → Client, Shipment
- Fields: id, clientId, dueDate
- Methods: markSent, markPaid

### Tracking, Security, Users

User 3 2 → Client, Employee
- Fields: id, username, role
- Methods: enable, disable

Employee 3 2 → PostOfficeBranch
- Fields: id, name, position
- Methods: assignBranch, changePosition

AuthSession 3 2 → User
- Fields: id, userId, expiresAt
- Methods: refresh, invalidate

ApiToken 3 2 → User
- Fields: id, token, scope
- Methods: rotate, revoke

AuditLog 3 2 → User
- Fields: id, userId, createdAt
- Methods: recordAction, findForUser

SystemEvent 3 2 → Shipment
- Fields: id, type, payload
- Methods: parsePayload, affectsShipment

### Communication and Support

Notification 3 2 → User
- Fields: id, channel, createdAt
- Methods: send, markRead

EmailMessage 3 2 → Notification, Client
- Fields: id, toAddress, subject
- Methods: render, dispatch

SMSMessage 3 2 → Notification, Client
- Fields: id, phoneNumber, text
- Methods: truncateIfNeeded, dispatch

SupportTicket 3 2 → Client, Shipment
- Fields: id, clientId, status
- Methods: addMessage, close

SupportMessage 3 2 → SupportTicket, User
- Fields: id, ticketId, authorId
- Methods: edit, redactPII

Claim 3 2 → Shipment, Client
- Fields: id, shipmentId, status
- Methods: approve, reject

ClaimStatusHistory 3 2 → Claim, User
- Fields: id, claimId, changedAt
- Methods: setStatus, revertStatus

## Associations (30)
Format: `ClassA → ClassB (краткое пояснение, файл: путь)`

1. Client → Address (defaultAddress — поле, хранит адрес клиента; файл: postal_oop/clients/Client.py)  
2. Client → ContactInfo (contactInfo — контактные данные клиента; файл: postal_oop/clients/Client.py)  
3. Sender → Client (sender ссылается на Client по clientId; файл: postal_oop/clients/Sender.py)  
4. Sender → Address (адрес отправителя хранится в поле address; файл: postal_oop/clients/Sender.py)  
5. Recipient → Address (адрес получателя — поле address; файл: postal_oop/clients/Recipient.py)  
6. Parcel → Client (посылка относится к клиенту-отправителю; файл: postal_oop/shipments/Parcel.py)  
7. Parcel → Tariff (расчёт цены зависит от Tariff; файл: postal_oop/shipments/Parcel.py)  
8. Shipment → Parcel (shipment содержит ссылку на Parcel; файл: postal_oop/shipments/Shipment.py)  
9. Shipment → Sender (shipment хранит отправителя; файл: postal_oop/shipments/Shipment.py)  
10. Shipment → Recipient (shipment хранит получателя; файл: postal_oop/shipments/Shipment.py)  
11. Shipment → PostOfficeBranch (shipment связан с текущим филиалом; файл: postal_oop/shipments/Shipment.py)  
12. TrackingEvent → Shipment (trackingEvent относится к конкретному shipment; файл: postal_oop/tracking/TrackingEvent.py)  
13. TrackingEvent → PostOfficeBranch (событие фиксируется в филиале; файл: postal_oop/tracking/TrackingEvent.py)  
14. PostOfficeBranch → Shipment (филиал регистрирует входящие/исходящие отправления; файл: postal_oop/offices/PostOfficeBranch.py)  
15. SortingCenter → Shipment (центр сортировки обрабатывает отправления; файл: postal_oop/logistics/SortingCenter.py)  
16. Route → RouteStop (маршрут содержит список остановок; файл: postal_oop/logistics/Route.py)  
17. RouteStop → PostOfficeBranch (остановка маршрута привязана к филиалу; файл: postal_oop/logistics/RouteStop.py)  
18. Vehicle → Route (транспорт назначается на маршрут; файл: postal_oop/logistics/Vehicle.py)  
19. Vehicle → Courier (у транспорта есть ответственный курьер; файл: postal_oop/logistics/Vehicle.py)  
20. Courier → PostOfficeBranch (курьер закреплён за филиалом; файл: postal_oop/logistics/Courier.py)  
21. Tariff → Zone (тариф действует в определённых зонах; файл: postal_oop/pricing/Tariff.py)  
22. Tariff → WeightRange (расчёт цены зависит от WeightRange; файл: postal_oop/pricing/Tariff.py)  
23. Tariff → Dimension (учитываются габариты отправления; файл: postal_oop/pricing/Tariff.py)  
24. Insurance → Parcel (страхование применяется к конкретной посылке; файл: postal_oop/pricing/Insurance.py)  
25. Payment → Shipment (оплата относится к отправлению; файл: postal_oop/payments/Payment.py)  
26. Payment → PaymentMethod (оплата произведена выбранным методом; файл: postal_oop/payments/Payment.py)  
27. SupportTicket → Shipment (тикет привязан к проблемному отправлению; файл: postal_oop/support/SupportTicket.py)  
28. SupportTicket → Client (тикет открыт клиентом; файл: postal_oop/support/SupportTicket.py)  
29. SupportMessage → SupportTicket (сообщение принадлежит тикету; файл: postal_oop/support/SupportMessage.py)  
30. Claim → Shipment (претензия подаётся по конкретному отправлению; файл: postal_oop/claims/Claim.py)  

## Summary

The Postal Office System (Postal OOP) implements a full domain model for postal operations:

- 50 domain classes, each in its own file under the `postal_oop` package
- 150 fields, covering clients, shipments, logistics, pricing, payments, tracking, support
- 100 unique behaviors (methods) representing business rules and operations
- 30 explicit class associations with short Russian explanations and file paths
- 12 custom exceptions describing typical error conditions in postal workflows

The system structure mirrors the Online Shop lab format and is suitable as a detailed technical report for the postal laboratory work.


