wordlist
========

Extremely simple RESTful word server in Flask. 
The server returns the JSON object { "Word": "random word" } when invoked.
JavaScript for an [Octopress][2] [aside][3] to call the service is included.
This is intended as the simplest example of a RESTful service, together with a [jQuery `$.ajax()`][4] call to invoke it.*

A demo is available  at [Public Sphere][1]

[1]: http://publicsphere.org
[2]: http://octopress.org/
[3]: http://octopress.org/docs/theme/template/
[4]: http://api.jquery.com/jQuery.ajax/
[5]: http://api.jquery.com/jQuery.get/

*A jQuery [`$.get()`][5] call could be substituted for `$.ajax()`.
