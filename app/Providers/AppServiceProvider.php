<?php

namespace App\Providers;

use App\Foundation\Git\GitRepository;
use App\Foundation\Storage\AppStorage;
use App\Services\Bitbucket\ApiService;
use App\Services\Git\GitService;
use Bitbucket\API\Http\Listener\OAuth2Listener;
use Bitbucket\API\Repositories\PullRequests;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    protected $defer = true;

    public function boot()
    {
        $this->app->singleton('Bitbucket', function () {
            $pull = new PullRequests();
            $pull->getClient()->addListener(
                new OAuth2Listener([
                    'client_id' => $this->app['config']->get('bitbucket.id'),
                    'client_secret' => $this->app['config']->get('bitbucket.secret'),
                ])
            );
            return new ApiService($pull, $this->app['config']->get('bitbucket.team'));
        });

        $this->app->singleton('GitClient', function () {
            return new GitService(
                $this->app->makeWith(
                    GitRepository::class,
                    ["repository" => $this->app['config']->get('git.repository_path')]
                )
            );
        });

        $this->app->singleton('AppStorage', function () {
            return new AppStorage($this->app);
        });
    }

    public function register()
    {
        return ['Bitbucket', 'GitClient', 'AppStorage'];
    }

    public function provides()
    {
        return [ApiService::class, GitService::class, AppStorage::class];
    }
}
