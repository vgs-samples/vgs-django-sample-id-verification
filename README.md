<p align="center"><a href="https://www.verygoodsecurity.com/"><img src="https://avatars0.githubusercontent.com/u/17788525" width="128" alt="VGS Logo"></a></p>
<p align="center"><b>vgs-django-pii-sample</b></p>
<p align="center"><i>Sample of using VGS for securing PII data(Django).</i></p>

## Requirements
- [Docker](https://www.docker.com/get-docker)
- [ngrok](https://ngrok.com/)
- account on [checkr.com](https://checkr.com/)

## Quick Start
1. Clone repository
2. Register on checkr.com
3. Put your `CHECKER_API_KEY` to `docker-compose.yml` file
4. Install docker on your local machine
4. Run `rerun.sh` script

Application will be started in Docker container and available at [http:localhost:8000/app/](http:localhost:8000/app/)

Application can work without VGS integration, it just stored all the PII (Personsally identifiable information) data in storage. 


## How to secure application with VGS
_before we start, we should make our app visible from internet. You can use ngrok for it._
<img src="images/run_ngrok.png">

Since we do not want to store PII data in our own storage, VGS can take data custodianship.
1. Go to [VGS-Dashboard](https://dashboard.verygoodsecurity.com), create a new organization, create a new vault. This is where we will store PII data.
2. Lets setup `inboud` traffic protection: 
  - go to `Routes`
  <img src="images/go_to_routes.png" width="256">
  
  - create new `inbound route`
  <img src="images/new_inbound_route.png" >
  
  - add `upstream` as an app host from `ngrok`
  <img src="images/inbound_setup_upstream.png" >
  
2.1 Lets setup filter which will redact PII data in client's request:
  - setup filter to process request data
  <img src="images/inbound_request_filter.png" >
  
2.2 To make data readable, lets setup another filter, that will reveal PII data in client's response:
  - add new filter in the `inbound` route
  <img src="images/add_next_filter.png" >
  
  - setup filter to process response data
  <img src="images/inbound_response_filter.png" >
  
**Done!**`Inbound` route is already created. Click `Save` button and check result.
  <img src="images/inbound_check_result.png" >

3 We've protected our system from storing PII data in our DB. But we need original data for processing it on [checkr.com](https://checkr.com/). Lets setup `outbound` routes to perform this operation.
  - go to `Routes`
  <img src="images/go_to_routes.png" width="256">
  
  - create new `outbound route`
  <img src="images/add_outbound_route.png" >
  
  - add `upstream` as a `checkr` API host
  <img src="images/outbound_setup_upstream.png" >
  
3.1 Let's setup filter which will reveal PII data in client's request to `Checkr`:
  - setup filter to process request data
  <img src="images/outbound_request_filter.png" >
  
3.2 `Checkr` service returns user's PII data in response, so we should rid of original PII data:
  - add new filter in the `outbound` route
  <img src="images/add_next_filter.png" >
  
  - setup filter to process response from `Checkr`
  <img src="images/outbound_response_filter.png" >
  
**Done!**`Outbound` route is already created. Click `Save` button and check result.
  <img src="images/outbound_check_result.png" >
  
4 We have created the VGS vault, lets use it in our app:
  - copy access urls to the vault
  <img src="images/proxy_urls.png" >
  
  - paste it to `/idVerification/settings.py`
  
  ```
  VGS_REVERSE_PROXY='https://tntvsu7b08w.SANDBOX.verygoodproxy.com' #inbound
  VGS_FORWARD_PROXY='https://US4HaDCukkzFFPcGe3nYR933:f0748f46-dcdd-4320-a7de-8f2204fef53a@tntvsu7b08w.SANDBOX.verygoodproxy.com:8080' #outbound
  ```
**Done! Our app is now secured by VGS. Lets check it out!**
- run `rerun.sh` script
- go to [http:localhost:8000/app/](http:localhost:8000/app/)
- add new data using UI form
<img src="images/add_new_data_page.png" >

- lets go to data original view and try to check it on `Checkr` service
<img src="images/check_data_page.png" >

  
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
