
import './timeline.css'

export function Timeline(props: { steps: { number: number, text: string, link?: string }[], completed: number, currentIndex: number, clickable: number[] | string }) {
    let { steps, completed, currentIndex, clickable } = props;

    completed = +completed;
    currentIndex = +currentIndex;
    // if clickable is a string, convert it to an array
    if (clickable === undefined) {
        clickable = [];
    } else if (typeof clickable === 'string') {
        clickable = clickable.split(',').map(Number);
    }

    return (
        <div className='timeline'>
            <div className="timeline-line"></div>
            <div className='timeline-circles'>
                {steps.map((step, index) => {
                    const position = index + 1;
                    const isCompleted = position <= completed;
                    const isCurrent = position === currentIndex;
                    clickable = clickable as number[];
                    const isClickable = clickable.includes(position);
                    console.log("clickable:", clickable,)
                    const isLast = position === steps.length - 1;

                    return (
                        <div className={`timeline-circle ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''} ${isLast ? 'last' : ''} ${isClickable ? 'clickable' : ''}`} key={step.number}>
                            {(isClickable) ?
                                <a href={step.link}>
                                    <div className='timeline-circle-number'>{step.number}</div>
                                    <div className='timeline-circle-text'>{step.text}</div>
                                </a>
                                :
                                <a>
                                    <div className='timeline-circle-number'>{step.number}</div>
                                    <div className='timeline-circle-text'>{step.text}</div>
                                </a>
                            }
                        </div>
                    );
                })}
            </div>
        </div >
    );
}