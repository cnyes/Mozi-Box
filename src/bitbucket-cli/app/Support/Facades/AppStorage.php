<?php

namespace App\Support\Facades;

use Illuminate\Support\Facades\Facade;

class AppStorage extends Facade
{
    protected static function getFacadeAccessor()
    {
        return 'AppStorage';
    }
}
