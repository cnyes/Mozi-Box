<?php

/*
 * Here goes the application configuration.
 */
return [
    /*
     * Here goes the application name.
     */
    'name' => 'Cnyes media team deployment tools',

    /*
     * Here goes the application version.
     */
    'version' => 'dev-master',

    /*
     * If true, development commands won't be available as the app
     * will be in the production environment.
     */
    'production' => false,

    /*
     * If true, scheduler commands will be available.
     */
    'with-scheduler' => false,

    /*
     * Here goes the application list of Laravel Service Providers.
     * Enjoy all the power of Laravel on your console.
     */
    'providers' => [
        App\Providers\AppServiceProvider::class,
    ],

    'commands' => [
        App\Commands\Bitbucket\PatchDiffCommand::class,
    ],

    'structure' => [
        'app' . DIRECTORY_SEPARATOR,
        'bootstrap' . DIRECTORY_SEPARATOR,
        'vendor' . DIRECTORY_SEPARATOR . '(?!(.*tests)).*\.php$',
        'config' . DIRECTORY_SEPARATOR,
        'composer.json',
    ],
];
