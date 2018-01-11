<?php

namespace Tests;

use Mockery;
use PHPUnit\Framework\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    protected $app;

    protected function setUp(): void
    {
        $this->initialApplication();
    }

    protected function tearDown(): void
    {
        $this->app = null;
        if (class_exists('Mockery')) {
            Mockery::close();
        }
    }

    protected function initialApplication(): void
    {
        $this->app = null;
        $this->app = $this->createApplication();
    }
}
