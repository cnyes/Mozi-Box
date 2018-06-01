<?php

namespace App\Support\Facades;

use Illuminate\Support\Facades\Facade;

class GitClient extends Facade
{
    protected static function getFacadeAccessor()
    {
        return 'GitClient';
    }
}
