import grpc
import time
from locust import TaskSet, User, between, task, events
from locust.exception import LocustError
from grpc_interceptor import ClientInterceptor
# for messages with 13 fields
import demo_pb2
import demo_pb2_grpc

# for messages with 26 fields
# import demo2_pb2 as demo_pb2
# import demo2_grpc as demo_pb2_grpc

# for messages with 52 fields
# import demo3_pb2 as demo_pb2
# import demo3_pb2_grpc as demo_pb2_grpc

from typing import Any, Callable
import time
from prometheus_client import Summary, start_http_server, Counter, Histogram

REQUEST_DURATION = Summary('request_processing_seconds', 'Time spent processing request')
requests_sent = Counter('grpc_requests_sent', 'Amount of sent requests')
REQUESTS_SUCCESS = Counter('requests_success_total', 'Number of successful requests')
REQUESTS_FAILURE = Counter('requests_failure_total', 'Number of failed requests')
histogram = Histogram('grpc_request_milliseconds_histrogram', 'Time spent processing grpc request')
INTERCEPTOR_DURATION = Summary('grpc_request_milliseconds_summary', 'Time spent processing grpc request')


start_http_server(22222)  # Replace 9090 with the desired port number for the Prometheus client to listen on


class LocustInterceptor(ClientInterceptor):
    def __init__(self, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = environment

    def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ):
        response = None
        exception = None
        start_perf_counter = time.perf_counter()
        response_length = 0
        try:
            response = method(request_or_iterator, call_details)
            response_length = response.result().ByteSize()
        except grpc.RpcError as e:
            exception = e

        self.env.events.request.fire(
            request_type="grpc",
            name=call_details.method,
            response_time=(time.perf_counter() - start_perf_counter) * 1000,
            response_length=response_length,
            response=response,
            context=None,
            exception=exception,
        )
        return response


class GrpcUsers(User):
    abstract = True
    stub_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for attr_value, attr_name in ((self.host, "host"), (self.stub_class, "stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")

        self._channel = grpc.insecure_channel("trackingservice:50052")
        interceptor = LocustInterceptor(environment=self.environment)
        self._channel = grpc.intercept_channel(self._channel, interceptor)

        self.stub = self.stub_class(self._channel)

class GrpcUser(TaskSet):
    @REQUEST_DURATION.time()
    @task
    def grpc_request(self):
        channel = grpc.insecure_channel("trackingservice:50052")
        self.stub = demo_pb2_grpc.TrackingServiceStub(channel)
        
        # this is the token for the mixed policy
        # token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwb2xpY3kiOnsiYWxsb3dlZCI6eyJjaXR5IjpbInN0cmluZyJdLCJjaXR5MiI6WyJzdHJpbmciXSwiY2l0eTMiOlsic3RyaW5nIl0sImNpdHk0IjpbInN0cmluZyJdLCJjb3VudHJ5IjpbInN0cmluZyJdLCJjb3VudHJ5MiI6WyJzdHJpbmciXSwiY291bnRyeTMiOlsic3RyaW5nIl0sImNvdW50cnk0IjpbInN0cmluZyJdLCJuYW1lIjpbInN0cmluZyJdLCJuYW1lMiI6WyJzdHJpbmciXSwibmFtZTMiOlsic3RyaW5nIl0sIm5hbWU0IjpbInN0cmluZyJdLCJwaG9uZSI6WyJzdHJpbmciXSwicGhvbmUyIjpbInN0cmluZyJdLCJwaG9uZTMiOlsic3RyaW5nIl0sInBob25lNCI6WyJzdHJpbmciXSwic3RyZWV0X25hbWUiOlsic3RyaW5nIl0sInN0cmVldF9uYW1lMiI6WyJzdHJpbmciXSwic3RyZWV0X25hbWUzIjpbInN0cmluZyJdLCJzdHJlZXRfbmFtZTQiOlsic3RyaW5nIl0sInN0cmVldF9udW1iZXIiOlsic3RyaW5nIl0sInN0cmVldF9udW1iZXIyIjpbInN0cmluZyJdLCJzdHJlZXRfbnVtYmVyMyI6WyJzdHJpbmciXSwic3RyZWV0X251bWJlcjQiOlsic3RyaW5nIl0sInppcF9jb2RlIjpbInN0cmluZyJdLCJ6aXBfY29kZTIiOlsic3RyaW5nIl0sInppcF9jb2RlMyI6WyJzdHJpbmciXSwiemlwX2NvZGU0IjpbInN0cmluZyJdfSwiZ2VuZXJhbGl6ZWQiOnsiY3JlZGl0X2NhcmRfY3Z2IjpbImludCIsIjMiXSwiY3JlZGl0X2NhcmRfY3Z2MiI6WyJpbnQiLCIzIl0sImNyZWRpdF9jYXJkX2N2djMiOlsiaW50IiwiMyJdLCJjcmVkaXRfY2FyZF9jdnY0IjpbImludCIsIjMiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl95ZWFyIjpbImludCIsIjEwIl0sImNyZWRpdF9jYXJkX2V4cGlyYXRpb25feWVhcjIiOlsiaW50IiwiMTAiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl95ZWFyMyI6WyJpbnQiLCIxMCJdLCJjcmVkaXRfY2FyZF9leHBpcmF0aW9uX3llYXI0IjpbImludCIsIjEwIl0sImNyZWRpdF9jYXJkX251bWJlciI6WyJzdHJpbmciLCI1Il0sImNyZWRpdF9jYXJkX251bWJlcjIiOlsic3RyaW5nIiwiNSJdLCJjcmVkaXRfY2FyZF9udW1iZXIzIjpbInN0cmluZyIsIjUiXSwiY3JlZGl0X2NhcmRfbnVtYmVyNCI6WyJzdHJpbmciLCI1Il19LCJub2lzZWQiOnsiYWdlIjpbImludCIsIkxhcGxhY2UiXSwiYWdlMiI6WyJpbnQiLCJMYXBsYWNlIl0sImFnZTMiOlsiaW50IiwiTGFwbGFjZSJdLCJhZ2U0IjpbImludCIsIkxhcGxhY2UiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl9tb250aCI6WyJpbnQiLCJMYXBsYWNlIl0sImNyZWRpdF9jYXJkX2V4cGlyYXRpb25fbW9udGgyIjpbImludCIsIkxhcGxhY2UiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl9tb250aDMiOlsiaW50IiwiTGFwbGFjZSJdLCJjcmVkaXRfY2FyZF9leHBpcmF0aW9uX21vbnRoNCI6WyJpbnQiLCJMYXBsYWNlIl19LCJyZWR1Y2VkIjp7ImVtYWlsIjpbInN0cmluZyIsIjQiXSwiZW1haWwyIjpbInN0cmluZyIsIjQiXSwiZW1haWwzIjpbInN0cmluZyIsIjQiXSwiZW1haWw0IjpbInN0cmluZyIsIjQiXX19LCJpc3MiOiJ0b2tlbkdlbmVyYXRvciIsImV4cCI6MTY5MDIwMjQ5N30.v-czbCQNGb3msqHKItmLOqHN1XJmP1ADC-yrvCPKm7dR1ZTtrMYV6Ox6n1f8XdGKriyqNGzvZ8adWLYS40SZgnIn0qWbDHwdAcfk9BZGsItGmI6OJewR_NRFnJF2lVQkeCvKMvb2O7UpK7ylhhmOh7Oo1mjMTCwHGyV2sM32Gj9Rwxnx7XlCDJ9AEBR5bA1BEAXokGk8i817dvJId6gljmc5Ga7cqnIAlxpQiEBfUs9lxSxrH9V3VaY_RuH_6qKiNy1w66kf3fjCE3Rgqh5Y_QTV-PAfe7W7i0H7g4oYhf22mfjGmfd2AqAVFf43CRfjCtQmvmcPKW_IFJ0XPg4C0A'
        
        # this is the token for the allow all policy
        # token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwb2xpY3kiOnsiYWxsb3dlZCI6eyJhZ2UiOlsic3RyaW5nIl0sImFnZTIiOlsic3RyaW5nIl0sImFnZTMiOlsic3RyaW5nIl0sImFnZTQiOlsic3RyaW5nIl0sImNpdHkiOlsic3RyaW5nIl0sImNpdHkyIjpbInN0cmluZyJdLCJjaXR5MyI6WyJzdHJpbmciXSwiY2l0eTQiOlsic3RyaW5nIl0sImNvdW50cnkiOlsic3RyaW5nIl0sImNvdW50cnkyIjpbInN0cmluZyJdLCJjb3VudHJ5MyI6WyJzdHJpbmciXSwiY291bnRyeTQiOlsic3RyaW5nIl0sImNyZWRpdF9jYXJkX2N2diI6WyJpbnQiXSwiY3JlZGl0X2NhcmRfY3Z2MiI6WyJpbnQiXSwiY3JlZGl0X2NhcmRfY3Z2MyI6WyJpbnQiXSwiY3JlZGl0X2NhcmRfY3Z2NCI6WyJpbnQiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl9tb250aCI6WyJpbnQiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl9tb250aDIiOlsiaW50Il0sImNyZWRpdF9jYXJkX2V4cGlyYXRpb25fbW9udGgzIjpbImludCJdLCJjcmVkaXRfY2FyZF9leHBpcmF0aW9uX21vbnRoNCI6WyJpbnQiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl95ZWFyIjpbImludCJdLCJjcmVkaXRfY2FyZF9leHBpcmF0aW9uX3llYXIyIjpbImludCJdLCJjcmVkaXRfY2FyZF9leHBpcmF0aW9uX3llYXIzIjpbImludCJdLCJjcmVkaXRfY2FyZF9leHBpcmF0aW9uX3llYXI0IjpbImludCJdLCJjcmVkaXRfY2FyZF9udW1iZXIiOlsic3RyaW5nIl0sImNyZWRpdF9jYXJkX251bWJlcjIiOlsic3RyaW5nIl0sImNyZWRpdF9jYXJkX251bWJlcjMiOlsic3RyaW5nIl0sImNyZWRpdF9jYXJkX251bWJlcjQiOlsic3RyaW5nIl0sImVtYWlsIjpbInN0cmluZyJdLCJlbWFpbDIiOlsic3RyaW5nIl0sImVtYWlsMyI6WyJzdHJpbmciXSwiZW1haWw0IjpbInN0cmluZyJdLCJuYW1lIjpbInN0cmluZyJdLCJuYW1lMiI6WyJzdHJpbmciXSwibmFtZTMiOlsic3RyaW5nIl0sIm5hbWU0IjpbInN0cmluZyJdLCJwaG9uZSI6WyJzdHJpbmciXSwicGhvbmUyIjpbInN0cmluZyJdLCJwaG9uZTMiOlsic3RyaW5nIl0sInBob25lNCI6WyJzdHJpbmciXSwic3RyZWV0X25hbWUiOlsic3RyaW5nIl0sInN0cmVldF9uYW1lMiI6WyJzdHJpbmciXSwic3RyZWV0X25hbWUzIjpbInN0cmluZyJdLCJzdHJlZXRfbmFtZTQiOlsic3RyaW5nIl0sInN0cmVldF9udW1iZXIiOlsic3RyaW5nIl0sInN0cmVldF9udW1iZXIyIjpbInN0cmluZyJdLCJzdHJlZXRfbnVtYmVyMyI6WyJzdHJpbmciXSwic3RyZWV0X251bWJlcjQiOlsic3RyaW5nIl0sInppcF9jb2RlIjpbInN0cmluZyJdLCJ6aXBfY29kZTIiOlsic3RyaW5nIl0sInppcF9jb2RlMyI6WyJzdHJpbmciXSwiemlwX2NvZGU0IjpbInN0cmluZyJdfSwiZ2VuZXJhbGl6ZWQiOnt9LCJub2lzZWQiOnt9LCJyZWR1Y2VkIjp7fX0sImlzcyI6InRva2VuR2VuZXJhdG9yIiwiZXhwIjoxNjkwMjA0NTMwfQ.Bx9DRaj5DrsO6tBSuth2jbwxdJZ8WqGRbFFcMXuv9x7XLVtx82Hsjj4l6cK_q1WwYSHllV9wgFAe25sSMGQAQApBMnI3Ng3S-Ce47cJdrzTF3S1UAMEAB4QhAqvMh0pr0_nUIlbXTugAadvgj5hOuxw5T57ZdXayGW9Uo-6IQuwreD-TwVHLftzIpLFXq3V0Y49Dv40rmf1pw6nKLbquCmed5bOOiDpe4aywudd866u9suTZVWkQyyvBIURudiBfiKRADpYMlMKcEfX2dz7y4iZyedWbp2FYfkDbMJZO31C5PahnSMksD3IyY-P9LjkNyjOMS8Rpz0fHVwlnW-WS4w'
        
        # this is the token for the deny all policy
        # token_all_denied = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwb2xpY3kiOnsiYWxsb3dlZCI6e30sImdlbmVyYWxpemVkIjp7fSwibm9pc2VkIjp7fSwicmVkdWNlZCI6e319LCJpc3MiOiJ0b2tlbkdlbmVyYXRvciIsImV4cCI6MTY5MDIwNTk4OX0.MKqRlpgurXR0nW2HZxvQEWBzRmZVuCovVAGz3gA5nrmey9G_shJ2ezJFO-Fs_PhzmSWqE2OUfS2Q4rgcSMUGRlqSIzF6NjvKU9S-gxTFbRWoedL1gM2MxandKfNvtaxjdINOxCPYR9l8X0SOEDMpxEoi8yLqM4p73LKlW7NIL2oyEVaGpnWD5YMPPmTtw5rXSyUW_PgVNP4Umlx8_e9eTeO6_gyaSkz0Ds4mPyYpwFTKNzYy6bQfve2hLY9Qx3z9eAsVvjH5pLfqPsF8VIlg8ajNRUMgv7v-4MAUbc0bsfrtTrSSml3Yql9Og2XPR7iv3ulbnw4l1Zx3IyMw3_qN7w'
        
        # this is the token for the maximize policy
        token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwb2xpY3kiOnsiYWxsb3dlZCI6e30sImdlbmVyYWxpemVkIjp7ImNpdHkiOlsic3RyaW5nIiwiMiJdLCJjaXR5MiI6WyJzdHJpbmciLCIyIl0sImNpdHkzIjpbInN0cmluZyIsIjIiXSwiY2l0eTQiOlsic3RyaW5nIiwiMiJdLCJjcmVkaXRfY2FyZF9jdnYiOlsiaW50IiwiMyJdLCJjcmVkaXRfY2FyZF9jdnYyIjpbImludCIsIjMiXSwiY3JlZGl0X2NhcmRfY3Z2MyI6WyJpbnQiLCIzIl0sImNyZWRpdF9jYXJkX2N2djQiOlsiaW50IiwiMyJdLCJjcmVkaXRfY2FyZF9leHBpcmF0aW9uX3llYXIiOlsiaW50IiwiMTAiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl95ZWFyMiI6WyJpbnQiLCIxMCJdLCJjcmVkaXRfY2FyZF9leHBpcmF0aW9uX3llYXIzIjpbImludCIsIjEwIl0sImNyZWRpdF9jYXJkX2V4cGlyYXRpb25feWVhcjQiOlsiaW50IiwiMTAiXSwiY3JlZGl0X2NhcmRfbnVtYmUyciI6WyJzdHJpbmciLCI1Il0sImNyZWRpdF9jYXJkX251bWJlciI6WyJzdHJpbmciLCI1Il0sImNyZWRpdF9jYXJkX251bWJlcjMiOlsic3RyaW5nIiwiNSJdLCJjcmVkaXRfY2FyZF9udW1iZXI0IjpbInN0cmluZyIsIjUiXSwiemlwX2NvZGUiOlsiaW50IiwiOCJdLCJ6aXBfY29kZTIiOlsiaW50IiwiOCJdLCJ6aXBfY29kZTMiOlsiaW50IiwiOCJdLCJ6aXBfY29kZTQiOlsiaW50IiwiOCJdfSwibm9pc2VkIjp7ImFnZSI6WyJpbnQiLCJMYXBsYWNlIl0sImFnZTIiOlsiaW50IiwiTGFwbGFjZSJdLCJhZ2UzIjpbImludCIsIkxhcGxhY2UiXSwiYWdlNCI6WyJpbnQiLCJMYXBsYWNlIl0sImNyZWRpdF9jYXJkX2V4cGlyYXRpb25fbW9udGgiOlsiaW50IiwiTGFwbGFjZSJdLCJjcmVkaXRfY2FyZF9leHBpcmF0aW9uX21vbnRoMiI6WyJpbnQiLCJMYXBsYWNlIl0sImNyZWRpdF9jYXJkX2V4cGlyYXRpb25fbW9udGgzIjpbImludCIsIkxhcGxhY2UiXSwiY3JlZGl0X2NhcmRfZXhwaXJhdGlvbl9tb250aDQiOlsiaW50IiwiTGFwbGFjZSJdLCJzdHJlZXRfbmFtZSI6WyJzdHJpbmciLCJMYXBsYWNlIl0sInN0cmVldF9uYW1lMiI6WyJzdHJpbmciLCJMYXBsYWNlIl0sInN0cmVldF9uYW1lMyI6WyJzdHJpbmciLCJMYXBsYWNlIl0sInN0cmVldF9uYW1lNCI6WyJzdHJpbmciLCJMYXBsYWNlIl0sInN0cmVldF9udW1iZXIiOlsiaW50IiwiTGFwbGFjZSJdLCJzdHJlZXRfbnVtYmVyMiI6WyJpbnQiLCJMYXBsYWNlIl0sInN0cmVldF9udW1iZXIzIjpbImludCIsIkxhcGxhY2UiXSwic3RyZWV0X251bWJlcjQiOlsiaW50IiwiTGFwbGFjZSJdfSwicmVkdWNlZCI6eyJjb3VudHJ5IjpbInN0cmluZyIsIjMiXSwiY291bnRyeTIiOlsic3RyaW5nIiwiMyJdLCJjb3VudHJ5MyI6WyJzdHJpbmciLCIzIl0sImNvdW50cnk0IjpbInN0cmluZyIsIjMiXSwiZW1haWwiOlsic3RyaW5nIiwiNCJdLCJlbWFpbDIiOlsic3RyaW5nIiwiNCJdLCJlbWFpbDMiOlsic3RyaW5nIiwiNCJdLCJlbWFpbDQiOlsic3RyaW5nIiwiNCJdLCJuYW1lIjpbInN0cmluZyIsIjQiXSwibmFtZTIiOlsic3RyaW5nIiwiNCJdLCJuYW1lMyI6WyJzdHJpbmciLCI0Il0sIm5hbWU0IjpbInN0cmluZyIsIjQiXSwicGhvbmUiOlsic3RyaW5nIiwiMyJdLCJwaG9uZTIiOlsic3RyaW5nIiwiMyJdLCJwaG9uZTMiOlsic3RyaW5nIiwiMyJdLCJwaG9uZTQiOlsic3RyaW5nIiwiMyJdfX0sImlzcyI6InRva2VuR2VuZXJhdG9yIiwiZXhwIjoxNjkwMjA3ODU2fQ.st2bNDh4QC5j6jdMZzNv_JkDWEyYjpfwp2EjzQHz2wbCGBWokZFGjYGddL-0I-K4WH_nWrOthjO8FAhLFpMO58Ztgrg5-w6PxNFwKEbbzozCTlpAvfmTCafXdIhiuQcAj9FcRwlv_MCAGleM0ExaLwaWJq80jmgpVs2zgU-TMMjafV_RMmkyBtFGEIXM62GGD8tQFKEjMA3YXXgrmM5Q08rRVF6CYG4StP9WqT_HGRX_tHHWdq59Nf5RqAb0y2RiUYMWRfNm-6HAuHkmvaT9USLI_3BEfoLiH2W7NqblBCu2wAFJzhQeggtd_kZKHIEGenaXkfPkxINdK4X_JZpNfQ'
        
        metadata = [('authorization', token)]
        start = round(time.time() * 1000.0)


        request_msg = demo_pb2.TrackingRequest(
            phone='030/1234567',
            street_name='Marchstr',
            street_number=23,
            zip_code=10383,
            city='Berlin',
            country='Germany',
            email='Test@mail.de',
            name='Mustermann',
            age=25,
            credit_card_number= "4432-8015-6152-0454",
            credit_card_cvv = 456,
            credit_card_expiration_year = 2024,
            credit_card_expiration_month = 10#,
            # phone2='030/1234567',
            # street_name2='Marchstr',
            # street_number2=23,
            # zip_code2=10383,
            # city2='Berlin',
            # country2='Germany',
            # email2='Test@mail.de',
            # name2='Mustermann',
            # age2=25,
            # credit_card_number2= "4432-8015-6152-0454",
            # credit_card_cvv2 = 456,
            # credit_card_expiration_year2 = 2024,
            # credit_card_expiration_month2 = 10,
            # phone3='030/1234567',
            # street_name3='Marchstr',
            # street_number3=23,
            # zip_code3=10383,
            # city3='Berlin',
            # country3='Germany',
            # email3='Test@mail.de',
            # name3='Mustermann',
            # age3=25,
            # credit_card_number3= "4432-8015-6152-0454",
            # credit_card_cvv3 = 456,
            # credit_card_expiration_year3 = 2024,
            # credit_card_expiration_month3 = 10,
            # phone4='030/1234567',
            # street_name4='Marchstr',
            # street_number4=23,
            # zip_code4=10383,
            # city4='Berlin',
            # country4='Germany',
            # email4='Test@mail.de',
            # name4='Mustermann',
            # age4=25,
            # credit_card_number4= "4432-8015-6152-0454",
            # credit_card_cvv4 = 456,
            # credit_card_expiration_year4 = 2024,
            # credit_card_expiration_month4 = 10
        )
        requests_sent.inc()
        response = self.stub.GetPersonaldata(request_msg, metadata=metadata)
        if response is not None: 
            REQUESTS_SUCCESS.inc()
        else: 
            REQUESTS_FAILURE.inc()
        end = round(time.time() * 1000.0)
        duration = end - start
        INTERCEPTOR_DURATION.observe(duration)
        histogram.observe(duration)
        print(duration)

class GrpcUser(GrpcUsers):
    stub_class = demo_pb2_grpc.TrackingServiceStub
    tasks = [GrpcUser]
    
