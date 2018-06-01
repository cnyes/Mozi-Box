<?php

namespace App\Commands\Bitbucket;

use App\Support\Facades\AppStorage;
use App\Support\Facades\Bitbucket;
use App\Support\Facades\GitClient;
use LaravelZero\Framework\Commands\Command;

class PatchDiffCommand extends Command
{
    protected $signature = 'bitbucket:patch-diff {project : bitbucket project where your PRs belong to.} {id* : PRs id arrays that you want to patch.}';
    protected $description = 'This command is trying to fetch & patch diff with multiple PRs with bitbucket.';

    public function __construct()
    {
        parent::__construct();
    }

    public function handle(): void
    {
        $ids = $this->argument('id');
        $project = $this->argument('project');

        foreach ($ids as $id) {
            $this->info(sprintf("fetch diff file By PR. Id = %s", $id));

            $diffPathFileName = "patch.diff";
            $diff = Bitbucket::getDiffByProjectAndPullRequestId($project, $id);
            $this->comment(sprintf("diff content = %s", $diff), "v");

            AppStorage::putTmp($diffPathFileName, $diff);

            $diffPatchFile = app_local_tmp_path($diffPathFileName);
            $this->comment(sprintf("Path file real path = %s", $diffPatchFile), "v");

            $this->info("begin to apply diff file.");
            GitClient::applyDiff($diffPatchFile);

            AppStorage::deleteTmp($diffPathFileName);
        }
    }
}
