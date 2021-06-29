# Load env
ENV=dev
ENVFILE=.make/$(ENV).rc
include $(ENVFILE)
export $(shell sed 's/=.*//' $(ENVFILE))

apply:
	# TODO: create pipelines

destroy:
	# TODO: delete pipelines

clean:
	find . -name "*.stg.ipynb" -type f -delete
	find . -name "papermill_notebook_run_handler.py" -type f -delete
	find . -name "outputs" -type d -print0 | xargs --no-run-if-empty -0 rm -r
	find . -name ".ipynb_checkpoints" -type d -print0 | xargs --no-run-if-empty -0 rm -r
	find . -name ".config" -type d -print0 | xargs --no-run-if-empty -0 rm -r