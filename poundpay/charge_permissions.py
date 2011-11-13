from .resource import Resource


class ChargePermissionError(Exception):
    pass


class ChargePermissionDeactivateError(ChargePermissionError):
    """Thrown when an error occurs while attempting to deactivate a payment
    """
    pass


_error_str_fmt = 'Charge permission status is {}. Only {} charge permissions may be {}'


class ChargePermission(Resource):
    """The charger permissions resource, represented by a RESTful resource located at
    ``/charge_permissions``.

    """
    _name = 'charge_permissions'

    def deactivate(self):
        """Deactivates a ``CREATED`` or ``ACTIVE`` charge permission.

        .. note::

           a :exc:`~poundpay.payments.PaymentEscrowError` is thrown if the
           Payment's status is ``INACTIVE``

        """
        if self.status == 'INACTIVE':
            msg = _error_str_fmt.format(self.status, 'CREATED or ACTIVE', 'deactivated')
            raise ChargePermissionDeactivateError(msg)

        self.status = 'INACTIVE'
        self.save()
