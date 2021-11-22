FROM python:3.9-slim
ADD create_dhcp_relay.py /
RUN python -m pip install firepyer
CMD [ "python", "create_dhcp_relay.py" ]