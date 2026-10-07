
"""发布配置

时间戳与版本号建议由 CI 在构建期注入环境变量 RELEASE_VERSION / RELEASE_TIME，
未注入时使用下方中性默认值，避免硬编码过期时间戳。
"""
import os

RELEASE_CONFIG = {
    'maintenance': {
        'is_maintenance': 0,
        'start_time': 0,
        'end_time': 0,
    },
    'release': {
        'hotfix_version_code': 1000000,
        'logout': 0,
        'version': os.environ.get('RELEASE_VERSION', '0.1.0'),
        'version_code': 1000000,
        'force_upgrade': 1000000,
    },
}
