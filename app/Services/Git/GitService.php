<?php

namespace App\Services\Git;

use App\Foundation\Git\GitRepository;

class GitService
{
    private $gitRepository = null;

    public function __construct(GitRepository $gitRepository)
    {
        $this->gitRepository = $gitRepository;
    }

    public function applyDiff(string $diffFilePath): bool
    {
        $this->gitRepository->checkBeforeApplyDiff($diffFilePath);
        $this->gitRepository->applyDiff($diffFilePath);
        return true;
    }
}
