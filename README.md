
Shiny-polished authentication
=============================

This was an attempt to configure shiny authentication using [polished](https://github.com/Tychobra/polished).
As described in their [README.md](https://github.com/Tychobra/polished/blob/master/README.md)
and in [their blog](https://www.tychobra.com/posts/2019_08_27_announcing_polished/),
we need a [firebase](https://firebase.google.com/) account in order to set up
the authentication system. Then in our app we need to provide our credentials
as described in the [firebase documentation](https://firebase.google.com/docs/storage/web/start).
This [project][https://github.com/shinyonfire/sof-auth-example] on github is an
example of authentication using *polished*. Firebase *keys* needs to be set in
`www/sof-auth.js` in order to work properly.

While this example seems working there is a poor documentation on polished and
in the authentication process itself. The authentication is managed by *JS* code
and is not clear to me how to reuse it for a custom application. Moreover, I didn't
find the *admin dashboard* described by the authors.

I will leave this as it is for now
