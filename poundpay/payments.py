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


_error_str_fmt = 'Payment state is {}. Only {} payments may be {}'


class Payment(Resource):
    """The Payment resource, represented by a RESTful resource located at
    ``/payments``.

    """
    _name = 'payments'

    @classmethod
    def batch_update(cls, *sids, **attrs):
        """Batch updates payments identified by `sids` with fields and values
        to specified by `attrs`.

        """
        attrs['sid'] = sids
        resp = cls.client.put(cls._name, attrs)
        payments = [Payment(**attrs) for attrs in resp.json[cls._name]]
        return payments

    def versions(self):
        """Retrieves the list of past versions of the payment.

        Each item in the list is itself a Payment object.
        """
        cls = self.__class__

        versions = cls.client.get(cls._get_path(self.sid) + '/history')
        versions_json = versions.json['payment_history']

        return [cls(**version) for version in versions_json]

    def escrow(self):
        """Escrows an ``AUTHORIZED`` payment by charging the authorized
        payment method associated with the ``AUTHORIZED`` payment

        .. note::

           a :exc:`~poundpay.payments.PaymentEscrowError` is thrown if the
           Payment's state is not ``AUTHORIZED``

        """
        if self.state != 'AUTHORIZED':
            msg = _error_str_fmt.format(self.state, 'AUTHORIZED', 'ESCROWED')
            raise PaymentEscrowError(msg)

        self.state = 'ESCROWED'
        self.save()

    def release(self):
        """Releases an ``ESCROWED`` payment by paying out the funds to
        a PoundPay account.

        .. note::

           a :exc:`~poundpay.payments.PaymentReleaseError` is thrown
           if the Payment's state is not ``ESCROWED``

        """
        if self.state != 'ESCROWED':
            msg = _error_str_fmt.format(self.state, 'ESCROWED', 'RELEASED')
            raise PaymentReleaseError(msg)

        self.state = 'RELEASED'
        self.save()

    def cancel(self):
        """
        Cancels a payment.

         - If the payment's state is ``ESCROWED``, it will refunding
           the payer. All PoundPay fees are refunded back to the
           developer.

         - If the payment's state is ``AUTHORIZED``, it will void the
           authorization.

         - If the payment's state is ``CREATED``, it will just mark
           the payment as canceled and no further operations can
           proceed on the payment.

        .. note::

           a :exc:`~poundpay.payments.PaymentCancelError` is thrown
           if the Payment's state is not in the appropriate state.

        """
        states = ('CREATED', 'AUTHORIZED', 'ESCROWED',)
        if self.state not in states:
            msg = _error_str_fmt.format(
                self.state,
                ', '.join(states),
                'CANCELED',
                )
            raise PaymentCancelError(msg)

        self.state = 'CANCELED'
        self.save()
