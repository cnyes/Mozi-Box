<?php

namespace App\Support\Facades;

use Illuminate\Support\Facades\Facade;

class Bitbucket extends Facade
{
    protected static function getFacadeAccessor()
    {
        return 'Bitbucket';
    }
}
