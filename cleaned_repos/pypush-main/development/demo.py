import apns
import ids

conn1 = apns.APNSConnection()
conn1.connect()


conn1.filter(["com.apple.madrid"])

# print(ids.lookup(conn1, ["mailto:jjtech@jjtech.dev"]))

# print(ids.register(conn1, "user_test2@icloud.com", "wowSecure1"))
