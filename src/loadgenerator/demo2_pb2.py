# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: demo2.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x64\x65mo2.proto\x12\x0bhipstershop\"0\n\x08\x43\x61rtItem\x12\x12\n\nproduct_id\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"F\n\x0e\x41\x64\x64ItemRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12#\n\x04item\x18\x02 \x01(\x0b\x32\x15.hipstershop.CartItem\"#\n\x10\x45mptyCartRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"!\n\x0eGetCartRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"=\n\x04\x43\x61rt\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12$\n\x05items\x18\x02 \x03(\x0b\x32\x15.hipstershop.CartItem\"\x07\n\x05\x45mpty\"B\n\x1aListRecommendationsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x13\n\x0bproduct_ids\x18\x02 \x03(\t\"2\n\x1bListRecommendationsResponse\x12\x13\n\x0bproduct_ids\x18\x01 \x03(\t\"\x84\x01\n\x07Product\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0f\n\x07picture\x18\x04 \x01(\t\x12%\n\tprice_usd\x18\x05 \x01(\x0b\x32\x12.hipstershop.Money\x12\x12\n\ncategories\x18\x06 \x03(\t\">\n\x14ListProductsResponse\x12&\n\x08products\x18\x01 \x03(\x0b\x32\x14.hipstershop.Product\"\x1f\n\x11GetProductRequest\x12\n\n\x02id\x18\x01 \x01(\t\"&\n\x15SearchProductsRequest\x12\r\n\x05query\x18\x01 \x01(\t\"?\n\x16SearchProductsResponse\x12%\n\x07results\x18\x01 \x03(\x0b\x32\x14.hipstershop.Product\"^\n\x0fGetQuoteRequest\x12%\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32\x14.hipstershop.Address\x12$\n\x05items\x18\x02 \x03(\x0b\x32\x15.hipstershop.CartItem\"8\n\x10GetQuoteResponse\x12$\n\x08\x63ost_usd\x18\x01 \x01(\x0b\x32\x12.hipstershop.Money\"_\n\x10ShipOrderRequest\x12%\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32\x14.hipstershop.Address\x12$\n\x05items\x18\x02 \x03(\x0b\x32\x15.hipstershop.CartItem\"(\n\x11ShipOrderResponse\x12\x13\n\x0btracking_id\x18\x01 \x01(\t\"a\n\x07\x41\x64\x64ress\x12\x16\n\x0estreet_address\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x04 \x01(\t\x12\x10\n\x08zip_code\x18\x05 \x01(\x05\"<\n\x05Money\x12\x15\n\rcurrency_code\x18\x01 \x01(\t\x12\r\n\x05units\x18\x02 \x01(\x03\x12\r\n\x05nanos\x18\x03 \x01(\x05\"8\n\x1eGetSupportedCurrenciesResponse\x12\x16\n\x0e\x63urrency_codes\x18\x01 \x03(\t\"N\n\x19\x43urrencyConversionRequest\x12 \n\x04\x66rom\x18\x01 \x01(\x0b\x32\x12.hipstershop.Money\x12\x0f\n\x07to_code\x18\x02 \x01(\t\"\x90\x01\n\x0e\x43reditCardInfo\x12\x1a\n\x12\x63redit_card_number\x18\x01 \x01(\t\x12\x17\n\x0f\x63redit_card_cvv\x18\x02 \x01(\x05\x12#\n\x1b\x63redit_card_expiration_year\x18\x03 \x01(\x05\x12$\n\x1c\x63redit_card_expiration_month\x18\x04 \x01(\x05\"e\n\rChargeRequest\x12\"\n\x06\x61mount\x18\x01 \x01(\x0b\x32\x12.hipstershop.Money\x12\x30\n\x0b\x63redit_card\x18\x02 \x01(\x0b\x32\x1b.hipstershop.CreditCardInfo\"(\n\x0e\x43hargeResponse\x12\x16\n\x0etransaction_id\x18\x01 \x01(\t\"R\n\tOrderItem\x12#\n\x04item\x18\x01 \x01(\x0b\x32\x15.hipstershop.CartItem\x12 \n\x04\x63ost\x18\x02 \x01(\x0b\x32\x12.hipstershop.Money\"\xbf\x01\n\x0bOrderResult\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x1c\n\x14shipping_tracking_id\x18\x02 \x01(\t\x12)\n\rshipping_cost\x18\x03 \x01(\x0b\x32\x12.hipstershop.Money\x12.\n\x10shipping_address\x18\x04 \x01(\x0b\x32\x14.hipstershop.Address\x12%\n\x05items\x18\x05 \x03(\x0b\x32\x16.hipstershop.OrderItem\"V\n\x1cSendOrderConfirmationRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\'\n\x05order\x18\x02 \x01(\x0b\x32\x18.hipstershop.OrderResult\"\xa3\x01\n\x11PlaceOrderRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x15\n\ruser_currency\x18\x02 \x01(\t\x12%\n\x07\x61\x64\x64ress\x18\x03 \x01(\x0b\x32\x14.hipstershop.Address\x12\r\n\x05\x65mail\x18\x05 \x01(\t\x12\x30\n\x0b\x63redit_card\x18\x06 \x01(\x0b\x32\x1b.hipstershop.CreditCardInfo\"=\n\x12PlaceOrderResponse\x12\'\n\x05order\x18\x01 \x01(\x0b\x32\x18.hipstershop.OrderResult\"!\n\tAdRequest\x12\x14\n\x0c\x63ontext_keys\x18\x01 \x03(\t\"*\n\nAdResponse\x12\x1c\n\x03\x61\x64s\x18\x01 \x03(\x0b\x32\x0f.hipstershop.Ad\"(\n\x02\x41\x64\x12\x14\n\x0credirect_url\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"\xca\x04\n\x0fTrackingRequest\x12\r\n\x05phone\x18\x01 \x01(\t\x12\x13\n\x0bstreet_name\x18\x02 \x01(\t\x12\x15\n\rstreet_number\x18\x03 \x01(\x05\x12\x10\n\x08zip_code\x18\x04 \x01(\x05\x12\x0c\n\x04\x63ity\x18\x05 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x06 \x01(\t\x12\r\n\x05\x65mail\x18\x07 \x01(\t\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x1a\n\x12\x63redit_card_number\x18\t \x01(\t\x12\x17\n\x0f\x63redit_card_cvv\x18\n \x01(\x05\x12#\n\x1b\x63redit_card_expiration_year\x18\x0b \x01(\x05\x12$\n\x1c\x63redit_card_expiration_month\x18\x0c \x01(\x05\x12\x0b\n\x03\x61ge\x18\r \x01(\x05\x12\x0e\n\x06phone2\x18\x0e \x01(\t\x12\x14\n\x0cstreet_name2\x18\x0f \x01(\t\x12\x16\n\x0estreet_number2\x18\x10 \x01(\x05\x12\x11\n\tzip_code2\x18\x11 \x01(\x05\x12\r\n\x05\x63ity2\x18\x12 \x01(\t\x12\x10\n\x08\x63ountry2\x18\x13 \x01(\t\x12\x0e\n\x06\x65mail2\x18\x14 \x01(\t\x12\r\n\x05name2\x18\x15 \x01(\t\x12\x1b\n\x13\x63redit_card_number2\x18\x16 \x01(\t\x12\x18\n\x10\x63redit_card_cvv2\x18\x17 \x01(\x05\x12$\n\x1c\x63redit_card_expiration_year2\x18\x18 \x01(\x05\x12%\n\x1d\x63redit_card_expiration_month2\x18\x19 \x01(\x05\x12\x0c\n\x04\x61ge2\x18\x1a \x01(\x05\"\xcb\x04\n\x10TrackingResponse\x12\r\n\x05phone\x18\x01 \x01(\t\x12\x13\n\x0bstreet_name\x18\x02 \x01(\t\x12\x15\n\rstreet_number\x18\x03 \x01(\x05\x12\x10\n\x08zip_code\x18\x04 \x01(\x05\x12\x0c\n\x04\x63ity\x18\x05 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x06 \x01(\t\x12\r\n\x05\x65mail\x18\x07 \x01(\t\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x1a\n\x12\x63redit_card_number\x18\t \x01(\t\x12\x17\n\x0f\x63redit_card_cvv\x18\n \x01(\x05\x12#\n\x1b\x63redit_card_expiration_year\x18\x0b \x01(\x05\x12$\n\x1c\x63redit_card_expiration_month\x18\x0c \x01(\x05\x12\x0b\n\x03\x61ge\x18\r \x01(\x05\x12\x0e\n\x06phone2\x18\x0e \x01(\t\x12\x14\n\x0cstreet_name2\x18\x0f \x01(\t\x12\x16\n\x0estreet_number2\x18\x10 \x01(\x05\x12\x11\n\tzip_code2\x18\x11 \x01(\x05\x12\r\n\x05\x63ity2\x18\x12 \x01(\t\x12\x10\n\x08\x63ountry2\x18\x13 \x01(\t\x12\x0e\n\x06\x65mail2\x18\x14 \x01(\t\x12\r\n\x05name2\x18\x15 \x01(\t\x12\x1b\n\x13\x63redit_card_number2\x18\x16 \x01(\t\x12\x18\n\x10\x63redit_card_cvv2\x18\x17 \x01(\x05\x12$\n\x1c\x63redit_card_expiration_year2\x18\x18 \x01(\x05\x12%\n\x1d\x63redit_card_expiration_month2\x18\x19 \x01(\x05\x12\x0c\n\x04\x61ge2\x18\x1a \x01(\x05\x32\xca\x01\n\x0b\x43\x61rtService\x12<\n\x07\x41\x64\x64Item\x12\x1b.hipstershop.AddItemRequest\x1a\x12.hipstershop.Empty\"\x00\x12;\n\x07GetCart\x12\x1b.hipstershop.GetCartRequest\x1a\x11.hipstershop.Cart\"\x00\x12@\n\tEmptyCart\x12\x1d.hipstershop.EmptyCartRequest\x1a\x12.hipstershop.Empty\"\x00\x32\x83\x01\n\x15RecommendationService\x12j\n\x13ListRecommendations\x12\'.hipstershop.ListRecommendationsRequest\x1a(.hipstershop.ListRecommendationsResponse\"\x00\x32\x83\x02\n\x15ProductCatalogService\x12G\n\x0cListProducts\x12\x12.hipstershop.Empty\x1a!.hipstershop.ListProductsResponse\"\x00\x12\x44\n\nGetProduct\x12\x1e.hipstershop.GetProductRequest\x1a\x14.hipstershop.Product\"\x00\x12[\n\x0eSearchProducts\x12\".hipstershop.SearchProductsRequest\x1a#.hipstershop.SearchProductsResponse\"\x00\x32\xaa\x01\n\x0fShippingService\x12I\n\x08GetQuote\x12\x1c.hipstershop.GetQuoteRequest\x1a\x1d.hipstershop.GetQuoteResponse\"\x00\x12L\n\tShipOrder\x12\x1d.hipstershop.ShipOrderRequest\x1a\x1e.hipstershop.ShipOrderResponse\"\x00\x32\xb7\x01\n\x0f\x43urrencyService\x12[\n\x16GetSupportedCurrencies\x12\x12.hipstershop.Empty\x1a+.hipstershop.GetSupportedCurrenciesResponse\"\x00\x12G\n\x07\x43onvert\x12&.hipstershop.CurrencyConversionRequest\x1a\x12.hipstershop.Money\"\x00\x32U\n\x0ePaymentService\x12\x43\n\x06\x43harge\x12\x1a.hipstershop.ChargeRequest\x1a\x1b.hipstershop.ChargeResponse\"\x00\x32h\n\x0c\x45mailService\x12X\n\x15SendOrderConfirmation\x12).hipstershop.SendOrderConfirmationRequest\x1a\x12.hipstershop.Empty\"\x00\x32\x62\n\x0f\x43heckoutService\x12O\n\nPlaceOrder\x12\x1e.hipstershop.PlaceOrderRequest\x1a\x1f.hipstershop.PlaceOrderResponse\"\x00\x32H\n\tAdService\x12;\n\x06GetAds\x12\x16.hipstershop.AdRequest\x1a\x17.hipstershop.AdResponse\"\x00\x32\x63\n\x0fTrackingService\x12P\n\x0fGetPersonaldata\x12\x1c.hipstershop.TrackingRequest\x1a\x1d.hipstershop.TrackingResponse\"\x00\x42\tZ\x07protos/b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'demo2_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\007protos/'
  _globals['_CARTITEM']._serialized_start=28
  _globals['_CARTITEM']._serialized_end=76
  _globals['_ADDITEMREQUEST']._serialized_start=78
  _globals['_ADDITEMREQUEST']._serialized_end=148
  _globals['_EMPTYCARTREQUEST']._serialized_start=150
  _globals['_EMPTYCARTREQUEST']._serialized_end=185
  _globals['_GETCARTREQUEST']._serialized_start=187
  _globals['_GETCARTREQUEST']._serialized_end=220
  _globals['_CART']._serialized_start=222
  _globals['_CART']._serialized_end=283
  _globals['_EMPTY']._serialized_start=285
  _globals['_EMPTY']._serialized_end=292
  _globals['_LISTRECOMMENDATIONSREQUEST']._serialized_start=294
  _globals['_LISTRECOMMENDATIONSREQUEST']._serialized_end=360
  _globals['_LISTRECOMMENDATIONSRESPONSE']._serialized_start=362
  _globals['_LISTRECOMMENDATIONSRESPONSE']._serialized_end=412
  _globals['_PRODUCT']._serialized_start=415
  _globals['_PRODUCT']._serialized_end=547
  _globals['_LISTPRODUCTSRESPONSE']._serialized_start=549
  _globals['_LISTPRODUCTSRESPONSE']._serialized_end=611
  _globals['_GETPRODUCTREQUEST']._serialized_start=613
  _globals['_GETPRODUCTREQUEST']._serialized_end=644
  _globals['_SEARCHPRODUCTSREQUEST']._serialized_start=646
  _globals['_SEARCHPRODUCTSREQUEST']._serialized_end=684
  _globals['_SEARCHPRODUCTSRESPONSE']._serialized_start=686
  _globals['_SEARCHPRODUCTSRESPONSE']._serialized_end=749
  _globals['_GETQUOTEREQUEST']._serialized_start=751
  _globals['_GETQUOTEREQUEST']._serialized_end=845
  _globals['_GETQUOTERESPONSE']._serialized_start=847
  _globals['_GETQUOTERESPONSE']._serialized_end=903
  _globals['_SHIPORDERREQUEST']._serialized_start=905
  _globals['_SHIPORDERREQUEST']._serialized_end=1000
  _globals['_SHIPORDERRESPONSE']._serialized_start=1002
  _globals['_SHIPORDERRESPONSE']._serialized_end=1042
  _globals['_ADDRESS']._serialized_start=1044
  _globals['_ADDRESS']._serialized_end=1141
  _globals['_MONEY']._serialized_start=1143
  _globals['_MONEY']._serialized_end=1203
  _globals['_GETSUPPORTEDCURRENCIESRESPONSE']._serialized_start=1205
  _globals['_GETSUPPORTEDCURRENCIESRESPONSE']._serialized_end=1261
  _globals['_CURRENCYCONVERSIONREQUEST']._serialized_start=1263
  _globals['_CURRENCYCONVERSIONREQUEST']._serialized_end=1341
  _globals['_CREDITCARDINFO']._serialized_start=1344
  _globals['_CREDITCARDINFO']._serialized_end=1488
  _globals['_CHARGEREQUEST']._serialized_start=1490
  _globals['_CHARGEREQUEST']._serialized_end=1591
  _globals['_CHARGERESPONSE']._serialized_start=1593
  _globals['_CHARGERESPONSE']._serialized_end=1633
  _globals['_ORDERITEM']._serialized_start=1635
  _globals['_ORDERITEM']._serialized_end=1717
  _globals['_ORDERRESULT']._serialized_start=1720
  _globals['_ORDERRESULT']._serialized_end=1911
  _globals['_SENDORDERCONFIRMATIONREQUEST']._serialized_start=1913
  _globals['_SENDORDERCONFIRMATIONREQUEST']._serialized_end=1999
  _globals['_PLACEORDERREQUEST']._serialized_start=2002
  _globals['_PLACEORDERREQUEST']._serialized_end=2165
  _globals['_PLACEORDERRESPONSE']._serialized_start=2167
  _globals['_PLACEORDERRESPONSE']._serialized_end=2228
  _globals['_ADREQUEST']._serialized_start=2230
  _globals['_ADREQUEST']._serialized_end=2263
  _globals['_ADRESPONSE']._serialized_start=2265
  _globals['_ADRESPONSE']._serialized_end=2307
  _globals['_AD']._serialized_start=2309
  _globals['_AD']._serialized_end=2349
  _globals['_TRACKINGREQUEST']._serialized_start=2352
  _globals['_TRACKINGREQUEST']._serialized_end=2938
  _globals['_TRACKINGRESPONSE']._serialized_start=2941
  _globals['_TRACKINGRESPONSE']._serialized_end=3528
  _globals['_CARTSERVICE']._serialized_start=3531
  _globals['_CARTSERVICE']._serialized_end=3733
  _globals['_RECOMMENDATIONSERVICE']._serialized_start=3736
  _globals['_RECOMMENDATIONSERVICE']._serialized_end=3867
  _globals['_PRODUCTCATALOGSERVICE']._serialized_start=3870
  _globals['_PRODUCTCATALOGSERVICE']._serialized_end=4129
  _globals['_SHIPPINGSERVICE']._serialized_start=4132
  _globals['_SHIPPINGSERVICE']._serialized_end=4302
  _globals['_CURRENCYSERVICE']._serialized_start=4305
  _globals['_CURRENCYSERVICE']._serialized_end=4488
  _globals['_PAYMENTSERVICE']._serialized_start=4490
  _globals['_PAYMENTSERVICE']._serialized_end=4575
  _globals['_EMAILSERVICE']._serialized_start=4577
  _globals['_EMAILSERVICE']._serialized_end=4681
  _globals['_CHECKOUTSERVICE']._serialized_start=4683
  _globals['_CHECKOUTSERVICE']._serialized_end=4781
  _globals['_ADSERVICE']._serialized_start=4783
  _globals['_ADSERVICE']._serialized_end=4855
  _globals['_TRACKINGSERVICE']._serialized_start=4857
  _globals['_TRACKINGSERVICE']._serialized_end=4956
# @@protoc_insertion_point(module_scope)
