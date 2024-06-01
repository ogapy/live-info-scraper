#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import 'source-map-support/register';
import { LiveInfoScraperStack } from '../lib/live-info-scraper-stack';
import { LiveInfoScraperProps } from '../lib/props';

const app = new cdk.App();
const env = {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION
};

new LiveInfoScraperStack(app, 'LiveInfoScraperStack', {
    env: env,
    dbName: 'mydatabase'
} as LiveInfoScraperProps);

