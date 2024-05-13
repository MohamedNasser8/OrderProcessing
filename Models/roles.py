from flask_principal import Permission, RoleNeed

#roles
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
