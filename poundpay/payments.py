from .resource import Resource

class PaymentError(Exception):
    pass

class PaymentEscrowError(PaymentError):
    pass

class PaymentReleaseError(PaymentError):
    pass

class PaymentCancelError(PaymentError):
    pass


class Payment(Resource):
    _name = 'payments'
    
    def escrow(self):
        if self.status != 'AUTHORIZED':
            raise PaymentEscrowError(
                "Payment status is %s.  " % self.status +
                "Only AUTHORIZED payments may be released")
        
        self.status = 'ESCROWED'
        self.save()

    def release(self):
        if self.status != 'ESCROWED':
            raise PaymentReleaseError(
                "Payment status is %s.  " % self.status +
                "Only ESCROWED payments may be released")
        self.status = 'RELEASED'
        self.save()

    def cancel(self):
        if self.status != 'ESCROWED':
            raise PaymentCancelError(
                "Payment status is %s.  " % self.status +
                "Only ESCROWED payments may be canceled")

        self.status = 'CANCELED'
        self.save()
