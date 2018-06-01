<?php

namespace Tests\Unit;

use App\Foundation\Git\GitRepository;
use App\Foundation\Storage\AppStorage;
use App\Providers\AppServiceProvider;
use App\Services\Bitbucket\ApiService;
use App\Services\Git\GitService;
use Mockery as m;
use Tests\TestCase;

class AppServiceProviderTest extends TestCase
{
    protected $provider = null;
    protected $container = null;

    public function setUp(): void
    {
        parent::setUp();
        $this->container = $this->app->getContainer();
        $this->container->bind(GitRepository::class, function () {
            return m::mock(GitRepository::class);
        });
        $this->provider = new AppServiceProvider($this->container);
    }

    public function testInstance()
    {
        $this->assertInstanceOf(AppServiceProvider::class, $this->provider);
    }

    public function testPerformBoot()
    {
        $this->provider->boot();
        $this->assertInstanceOf(ApiService::class, $this->container->make('Bitbucket'));
        $this->assertInstanceOf(GitService::class, $this->container->make('GitClient'));
        $this->assertInstanceOf(AppStorage::class, $this->container->make('AppStorage'));
    }

    public function testNoPerformRegister()
    {
        $this->assertEquals($this->provider->register(), ['Bitbucket', 'GitClient', 'AppStorage']);
    }

    public function testNoPerformProvides()
    {
        $this->assertEquals(
            $this->provider->provides(),
            [ApiService::class, GitService::class, AppStorage::class]
        );
    }
}
