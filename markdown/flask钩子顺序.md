flask钩子函数执行顺序：

```mermaid
graph TD

a[blue_print.before_app_first_request] 
b[app.before_request]
a --> b
c[blue_print.before_app_request]
b --> c
ee[app.errorhandler]
c --> ee
d[blue_print.after_request]
ee --> d
e[blue_print.after_app_request]
d --> e
f[app.after_request]
e --> f
g[app.teardown_request]
f --> g
h[app.teardown_appcontext]
g --> h
```

flask中有三种异常处理的钩子，`app.errorhandler`、`blueprint.errorhandler`和`blueprint.app_errorhandler`，在处理时，只会调用其中一个，优先级为

`blueprint.errorhandler` > `blueprint.app_errorhandler` > `app.errorhandler`

