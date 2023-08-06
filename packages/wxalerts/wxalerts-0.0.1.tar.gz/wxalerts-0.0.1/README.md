# wxalerts

Simple monke code that scans a state every 30 seconds for weather alerts.

This will be updated in the future to be cleaner and have more features.

---

```python
import wxalerts

# scan for a state
wxalerts.start(state="OR")
```

## Options
```
refresh         :   bool, tells the class if it should
                    redo the scan

                    default value: True

refresh_time    :   int, tells the class how many seconds
                    it should wait before refreshing
                    (only works if refresh is True)

                    default value: 30

refresh_count   :   int, tells the class how many times to
                    refresh. Set to 0 if you want infinite
                    (only works if refresh is True)

                    default value: 5

state           :   str, tells the class what state to scan
                    for (1), initials only, IL, OR, FL, and
                    so on

                    default value: None
```
