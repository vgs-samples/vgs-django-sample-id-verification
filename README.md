[![CircleCI](https://circleci.com/gh/verygoodsecurity/vgs-django-sample-id-verification.svg?style=svg)](https://circleci.com/gh/verygoodsecurity/vgs-django-sample-id-verification)

<p align="center"><a href="https://www.verygoodsecurity.com/"><img src="https://avatars0.githubusercontent.com/u/17788525" width="128" alt="VGS Logo"></a></p>
<p align="center"><b>vgs-django-pii-sample</b></p>
<p align="center"><i>Sample of using VGS for securing PII data(Django).</i></p>

# Instructions for using this App
This demo app demonstrates a typical scenario for secure/revealing traffic from customer application to a payments operator.

## Requirements
- Installed [Docker](https://www.docker.com/get-docker)
- Installed [ngrok](https://ngrok.com/)
- Account on [checkr.com](https://checkr.com/)

## First Start
1. Clone this repository
2. Ensure both `INBOUND_ROUTE` and `OUTBOUND_ROUTE` in `idVerification/settings.py` are empty.
 2.1 Ensure `VGS_INBOUND_URL` in `docker-compose.yml` is set to `http://vgs-django-sample:8000`. [Why we use Nginx](https://github.com/verygoodsecurity/vgs-django-sample-id-verification#why-we-use-nginx)
3. Set your `CHECKER_API_KEY` in `docker-compose.yml`
4. Run `rerun.sh` script

Application will be started in a Docker container and available at [http://localhost:8001/app/](http://localhost:8001/app/)

Before integrating with VGS, the application works but it stores all PII (Peronsally identifiable information) data in storage.

### Ngrok and Django

1. Force `ngrok` to specify a fixed host name via the command-line `-host-header` flag:

```sh
ngrok http -bind-tls=true -subdomain=vgssl5 -host-header=${VGS_TENANT_IDENTIFER}.sandbox.verygoodproxy.com 8000

```

*NOTE:* Can also simply create a random subdomain without using the static paid feature above for `ngrok`

```sh
ngrok http 8000
```

2. Please set the follow flag in django’s `settings.py`:

```python
ALLOWED_HOSTS = ['localhost', '.verygoodproxy.com']
```

Once these configurations are set, `ngrok` and `django` play nicely together.

## How to secure application with VGS

To make the local application visible from internet run ngrok `ngrok http 8000`(not `8001` - used by Nginx). Use ngrok URI for setting up inbound route.
<img src="images/inbound.gif" >
1. Go to [VGS-Dashboard](https://dashboard.verygoodsecurity.com), create a new organization, create a new vault. This is where we will store PII data.
2. Setup `inboud` traffic protection:
    - go to `Routes`
    - create new inbound route: `Add new route` -> `New inbound route`
    - set `Upstream Host` to the `ngrok` endpoint from above (e.g. `https://<some id>.ngrok.io` -> localhost:8000)
3. Setup redact on request filter to protected our system from storing PII data in our DB:
    - `Conditions`:
        - `HTTP Method` `equals` `POST`
        - `Pathinfo` `equals` `/app/add`
    - `Phase` `On request`
    - `REDACT`
    - `Form`
        - `Fields in FormData`
            - `SSN`
            - `driver_license_number`
    - leave all other fields with by default value
4. To make data readable for the customer who owns this data, lets `Add filter`, that will reveal PII data in client's response:
    - add new filter in the `inbound` route
    - `Conditions`:
        - `Pathinfo` `begins with` `/app/api/data`
        - `HTTP Method` `equals` `GET`
        - `ContentType` `equals` `application/json`
    - `Phase` `On response`
    - `REVEAL`
    - `Json`
        - `Fields in JSON path`
            - `$.social_security_number`
            - `$.driver_license_number`
    - leave all other fields with by default value
5. Click `Save` button and check result of _Inbound_ routes creation in `Routes`.
  <img src="images/inbound_check_result.png" >
Next we are going to create Outbound route.
  <img src="images/outbound.gif" >

6. Setup `outbound` route for processing original data on [checkr.com](https://checkr.com/).
    - go to `Routes`
    - create new outbound route: `Add new route` -> `New outbound route`
    - set `Upstream Host` with `checkr` API host `api.checkr.com`
7. Setup filter for revealing PII data in client's request to `Checkr`:
   - `Conditions`:
      - `Pathinfo` `equals` `/v1/candidates`
      - `HTTP Method` `equals` `POST`
   - `Phase` `On request`
   - `REVEAL`
   - `Json`
    - `Fields in JSON path`
        - `$.ssn`
        - `$.driver_license_number`
   - leave all other field values as is
8. To get rid of storing user's PII data from `Checkr` service response add new `REDACT` `on response` filter in the `outbound` route
   - `Conditions`:
        - `Pathinfo` `equals` `/v1/candidates`
   - `Phase` `On response`
   - `REDACT`
   - `Json`
    - `Fields in JSON path`
        - `$.ssn`
        - `$.driver_license_number`

9. Click `Save` button and check the result of _Outbound_ routes creation in `Routes`.
  <img src="images/outbound_check_result.png" >

10. Use `Vault URLs` it in our app:
  <img src="images/proxy_urls.png" >

  - copy the URLS `docker-compose.yml` [Why we use Nginx](https://github.com/verygoodsecurity/vgs-django-sample-id-verification#why-we-use-nginx)
  ```
  INBOUND_ROUTE='https://tntdbopmilp.SANDBOX.verygoodproxy.com' #inbound
  ```
  and to `/idVerification/settings.py`
  ```
  OUTBOUND_ROUTE='https://US2yjMXkaJddDpxSCj1BCFb7:056c520b-5564-4750-bb96-d774104090e0@tntdbopmilp.SANDBOX.verygoodproxy.com:8080' #outbound
  ```
11. Our app is now secured by VGS. Lets check it out.
- restart `rerun.sh` script
- go to [http://localhost:8001/app/](http://localhost:8001/app/)
- add new data using UI form
- go to data original view and try to check it on `Checkr` service
<img src="images/django_demo.gif" >

## Why we use Nginx
Sample application has [CSRF protection](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)). Protection based on 2 tockens that generated/verified by Django server. One of them stores in browser cookies, so we need same host for django server and VGS proxy to allow browser add CSRF cookie to VGS proxy request.

How it works:

<img src="images/django_reverse_proxy_with_csrf.png" >


## What is VGS?

_**Want to just jump right in?** Check out our [getting started
guide](https://www.verygoodsecurity.com/docs/getting-started)._

Very Good Security (VGS) allows you to enhance your security standing while
maintaining the utility of your data internally and with third-parties. As an
added benefit, we accelerate your compliance certification process and help you
quickly obtain security-related compliances that stand between you and your
market opportunities.

To learn more, visit us at https://www.verygoodsecurity.com/

## License

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file
for details.
