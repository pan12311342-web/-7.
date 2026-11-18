import time
from .image_utils import prepare_image
from .model import extract
from .rules import validate

def process(data: bytes):
    t0=time.perf_counter()
    prepared,before,after=prepare_image(data)
    prep=time.perf_counter()-t0
    t1=time.perf_counter()
    invoice, model_time, tokens=extract(prepared)
    extraction=time.perf_counter()-t1
    t2=time.perf_counter()
    problems, decision=validate(invoice)
    validation=time.perf_counter()-t2
    return {
        "invoice": invoice.model_dump(mode="json"),
        "decision": decision,
        "problems": problems,
        "meta": {"before": before, "after": after, "prepare_sec": prep,
                 "extraction_sec": extraction, "validation_sec": validation,
                 "model_sec": model_time, "tokens": tokens}
    }
