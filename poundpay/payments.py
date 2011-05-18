from .resource import Resource


class PaymentError(Exception):
    pass


class PaymentEscrowError(PaymentError):
    """Thrown when an error occurs while attempting to ESCROW a payment

    """
    pass


class PaymentReleaseError(PaymentError):
    """Thrown when an error occurs while attempting to RELEASE a payment

    """
    pass


class PaymentCancelError(PaymentError):
    """Thrown when an error occurs while attempting to CANCEL a payment

    """
    pass


_error_str_fmt = 'Payment status is {}. Only {} payments may be {}'


class Payment(Resource):
    """The Payment resource, represented by a RESTful resource located at
    ``/payments``.

    """
    _name = 'payments'
    
    def versions(self):
        """Retrieves the list of past versions of the payment.
        
        Each item in the list is itself a Payment object.
        """
        cls = self.__class__
        
        versions = cls.client.get(cls._get_path(self.sid) + '?versions=all')
        versions_json = versions.json['payments']
        
        return [cls(**version) for version in versions_json]
    
    def escrow(self):
        """Escrows an ``AUTHORIZED`` payment by charging the authorized
        payment method associated with the ``AUTHORIZED`` payment

        .. note::

           a :exc:`~poundpay.payments.PaymentEscrowError` is thrown if the
           Payment's status is not ``AUTHORIZED``

        """
        if self.status != 'AUTHORIZED':
            msg = _error_str_fmt.format(self.status, 'AUTHORIZED', 'ESCROWED')
            raise PaymentEscrowError(msg)

        self.status = 'ESCROWED'
        self.save()

    def release(self):
        """Releases an ``ESCROWED`` payment by paying out the funds to
        a PoundPay account.

        .. note::

           a :exc:`~poundpay.payments.PaymentReleaseError` is thrown
           if the Payment's status is not ``ESCROWED``

        """
        if self.status != 'ESCROWED':
            msg = _error_str_fmt.format(self.status, 'ESCROWED', 'RELEASED')
            raise PaymentReleaseError(msg)

        self.status = 'RELEASED'
        self.save()

    def cancel(self):
        """Cancels an ``ESCROWED`` payment by refunding the payer. All
        PoundPay fees are refunded back to the developer, as well.

        .. note::

           a :exc:`~poundpay.payments.PaymentCancelError` is thrown
           if the Payment's status is not ``ESCROWED``

        """
        if self.status != 'ESCROWED':
            msg = _error_str_fmt.format(self.status, 'ESCROWED', 'CANCELED')
            raise PaymentCancelError(msg)

        self.status = 'CANCELED'
        self.save()
