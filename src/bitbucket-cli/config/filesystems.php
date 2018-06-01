<?php

return [
    'default' => 'app_local',

    'disks' => [
        'app_local' => [
            'driver' => 'local',
            'root' => env('APP_TMP_DIR', env('HOME') . DIRECTORY_SEPARATOR . '.cnyesDeploymentCli.d'),
        ],
    ],
];
