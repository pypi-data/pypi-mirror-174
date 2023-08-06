# WEBFLEET.connect 

This library enables you to interact with WEBFLEETs developer API called [WEBFLEET.connect](https://portals.webfleet.com/s/article/WEBFLEET-connect-API-documentation)

## Quick Start

```
api = WfConnect(self.url)
api.setAuthentication(
    self.account,
    self.username,
    self.password,
)
...
vehicles = api.showObjectReportExtern("your-group-name")
```
