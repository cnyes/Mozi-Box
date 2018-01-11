<?php

namespace App\Services\Bitbucket;

use Bitbucket\API\Repositories\PullRequests;

class ApiService
{

    private $pullOperator = null;
    private $team = null;

    public function __construct(PullRequests $pullOperator, string $team)
    {
        $this->pullOperator = $pullOperator;
        $this->team = $team;
    }

    public function getDiffByProjectAndPullRequestId(string $project, string $pullRequestId): string
    {
        return $this->pullOperator->diff($this->team, $project, $pullRequestId)->getContent();
    }
}
