# motherduck-show-n-tell

Welcome to BuildFlow!

This is a simple example of serving the string "Hello World!" from a service [endpoint](https://docs.launchflow.com/buildflow/programming-guide/endpoints)

If you want to get started quickly you can run your application with:

```
buildflow run
```

Then you can visit http://localhost:8000 to see your application running.

## Directory Structure

At the root level there are three important files:

- `buildflow.yml` - This is the main configuration file for your application. It contains all the information about your application and how it should be built.
- `main.py` - This is the entry point to your application and where your `Flow` is initialized.
- `requirements.txt` - This is where you can specify any Python dependencies your application has.

Below the root level we have:

**motherduck-show-n-tell**

This is the directory where your application code lives. You can put any files you want in here and they will be available to your application. We create a couple directories and files for you:

- **processors**: This is where you can put any custom processors you want to use in your application. In here you will see we have defined a _service.py_ for a service in your application and a _hello_world.py_ file for a custom [endpoint](https://docs.launchflow.com/buildflow/programming-guide/endpoints) processor.
- **primitives.py**: This is where you can define any custom [primitive](https://docs.launchflow.com/buildflow/programming-guide/primitives) resources that your application will need. Note it is empty right now since your initial application is so simple.
- **dependencies.py**: This is where you can define any custom [dependencies](https://docs.launchflow.com/buildflow/programming-guide/dependencies) you might need.
- **settings.py**: This file loads in our environment variables and makes them available to our application.

**.buildflow**

This is a hidden directory that contains all the build artifacts for your application. You can general ignore this directory and it will be automatically generated for you. If you are using github you probably want to put this in your _.gitignore_ file.

## Customizing your application

You application is pretty simple now but you can customize it to do anything you want. Here are some ideas:

- Attach [primitives](https://docs.launchflow.com/buildflow/programming-guide/primitives) to your application to add resources like [databases](https://docs.launchflow.com/buildflow/primitives/gcp/cloud_sql), [queues](https://docs.launchflow.com/buildflow/primitives/aws/sqs), [buckets](https://docs.launchflow.com/buildflow/primitives/aws/s3), or [data warehouses](https://docs.launchflow.com/buildflow/primitives/gcp/bigquery)
- Use [depedencies](https://docs.launchflow.com/buildflow/programming-guide/dependencies) to attach dependencies to your processors. Such as [google auth](https://docs.launchflow.com/buildflow/dependencies/auth#authenticated-google-user), [SQLAlchemy Session](https://docs.launchflow.com/buildflow/dependencies/sqlalchemy), or push data to a [sink](https://docs.launchflow.com/buildflow/dependencies/sink)
- Add additional processors for [async processing](https://docs.launchflow.com/buildflow/programming-guide/consumers) or [data ingestion](https://docs.launchflow.com/buildflow/programming-guide/collectors)
- Manage your entire stack with [BuildFlow's pulumi integration](https://docs.launchflow.com/buildflow/programming-guide/buildflow-yaml#pulumi-configure)
