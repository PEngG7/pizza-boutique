import grpc
import time
from locust import TaskSet, User, between, task, events
from locust.exception import LocustError
from grpc_interceptor import ClientInterceptor
import demo_pb2
import demo_pb2_grpc
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
        token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwb2xpY3kiOnsiYWxsb3dlZCI6eyJjaXR5IjpbInN0cmluZyJdLCJjb3VudHJ5IjpbInN0cmluZyJdLCJjcmVkaXRfY2FyZF9jdnYiOlsiaW50Il0sImNyZWRpdF9jYXJkX2V4cGlyYXRpb25fbW9udGgiOlsiaW50Il0sImNyZWRpdF9jYXJkX2V4cGlyYXRpb25feWVhciI6WyJpbnQiXSwiY3JlZGl0X2NhcmRfbnVtYmVyIjpbInN0cmluZyJdLCJlbWFpbCI6WyJzdHJpbmciXSwibmFtZSI6WyJzdHJpbmciXSwicGhvbmUiOlsic3RyaW5nIl0sInN0cmVldF9uYW1lIjpbInN0cmluZyJdLCJzdHJlZXRfbnVtYmVyIjpbInN0cmluZyJdLCJ6aXBfY29kZSI6WyJzdHJpbmciXX0sImdlbmVyYWxpemVkIjp7fSwibm9pc2VkIjp7fSwicmVkdWNlZCI6e319LCJpc3MiOiJ0b2tlbkdlbmVyYXRvciIsImV4cCI6MTY4OTc4MjEwNn0.iFeRm5bxjcsWpyPt2Y2N-ZgqIublK9Ntk742krZYjeH1i_gugAf7YkOB6lKnUkKAUATJiFXbhn99WevDc9huqzI93b3YiIbLNwdijOv3KNg-xI75njr-_abJngeME6wHG9ZJPbbQaU2zAia1ASTn2cfzrGuGUrreMhzZ_fmugk9wYPYH6mFSc9Ir88jdSQgRPTvCcdDsgUq4EDt_XsrS0dbYPHVGP8XerRt47ypR0nxPZuj4XWflPs_PaecvW3HJTrCTLTkcJRYxrm0aKeblb0HMlfoRZXyp6CUoEX4qINf3TGNvbxYDA7TPlJkWj7R7QDyz2sLVF505fRFb4r998Q'
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
            age=25
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
    
