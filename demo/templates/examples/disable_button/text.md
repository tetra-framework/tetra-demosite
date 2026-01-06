---
title: Disable submit button
---

# Disable submit button

When submitting a form, many users tend to double-click the `submit` button, leading to double entries in the databases, if the timing was right ;-)

It is an easy pattern to just disabling the button right after clicking it. You can do two things in the `@click` listener: disable the button *and* call `submit()`.

{% md_include_source "demo/components/examples/disable_button/disable_button.html" %}

If you click the button, it is disabled without altering the server state. When the component is reloaded, the button is enabled again (for a create form), but mostly, you will redirect to another page using `self.client._redirect(...)` 

In this demo, the component method `submit()` simply returns after a 3 seconds delay.

The `sleep(3)` function simulates a long-running operation, such as a database query or an API call, that takes a few seconds to complete. This allows the user to see the button disabled for a few seconds, giving them feedback that their action has been received and processed.

Fow longer delays, you can also use a [loading spinner](/examples/spinner).